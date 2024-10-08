import re
import os
from .model import _get_model
from .state import AgentState
from .utils import extract_code
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


prompt = """You are tasked to write documentation as the user request.
The documentation that you write must be contextualized, because this code and documentation belong to a big project and must work in relation with other file.
The user will give you some information about the project to better contextualize and help you on the task.


tech language: {TECH_LANGUAGE}
tech framework: {TECH_FRAMEWORK}

<requirements>
{REQUIREMENTS}
</requirements>

<tech_requirements>
{TECH_REQUIREMENTS}
</tech_requirements>


Please generate this documentation using .md syntax.
"""

prompt_user = """This is the description of the code that you must generate documentation for:
<code_file_name>
{CODE_FULL_PATH}
</code_file_name>

<code_description>
{CODE_DESCRIPTION}
</code_description>

<code>
{CODE}
</code>
"""


def write_documentation(state: AgentState, files) -> str:
    """
    Generate a consolidated documentation text based on the files' description in a multi-threaded way.
    Each file is processed on a separate thread, and the documentation is accumulated in a single text variable.

    :param state: Contains the current agent's state, including file descriptions.
    :param files: A list of dictionaries, each containing 'full_path', 'file_description', and 'code'.
    :return: A single string containing the documentation for all files.
    """

    # Initialize the LLM model
    model = _get_model()

    # Variable to hold the entire documentation text
    full_documentation_text = ""

    def process_file(file):
        full_path = file['full_path']
        file_description = file['file_description']
        file_code = file['code']

        # Prepare the LLM prompt for generating documentation
        messages = [
            {"role": "system", "content": prompt.format(TECH_LANGUAGE=state.get('input').get('tech_language'),
                                                        TECH_FRAMEWORK=state.get('input').get('tech_framework'),
                                                        REQUIREMENTS=state.get('requirements'),
                                                        TECH_REQUIREMENTS=state.get('technical_requirements'))},
            {"role": "user",
             "content": prompt_user.format(CODE=file_code, CODE_FULL_PATH=full_path, CODE_DESCRIPTION=file_description)}
        ]

        try:
            # Invoke the model to generate the documentation based on the file description
            response = model.invoke(messages)
            documentation = response.content

            file['documentation'] = documentation

            # Prepare the documentation section for this file
            file_documentation = f"## Documentation for {os.path.basename(full_path)}\n"
            file_documentation += f"**Path**: {full_path}\n\n"
            file_documentation += f"{documentation}\n\n"

            return file_documentation

        except Exception as e:
            print(f"Error generating documentation for {full_path}: {e}")
            return ""

    # Use ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor() as executor:
        # Submit each file for processing in a separate thread
        futures = {executor.submit(process_file, file): file for file in files}

        # Wait for all threads to complete and collect the results
        for future in as_completed(futures):
            full_documentation_text += future.result()  # Append the generated documentation

    return full_documentation_text


prompt_2 = """You are tasked to re-write a documentation.
The user will give a documentation that must be re-written in a more professional way and organized avoiding any kind of ambiguity and confusion.
Probably the user will give you the path of each file that is documented, you must keep this part of the path and link to the real file.

Please generate this documentation using .md syntax.
IMPORTANT: Use only the markdown syntax there is no reason to start your output with '```markdown' or '```' at the end. <- IMPORTANT.
"""

prompt_user_2 = """Rewrite the documentation:

<documentation>
{documentation}
</documentation>
"""


def rewrite_documentation(documentation: str) -> str:
    """
    Rewrite the documentation provided by the user in a more professional way.
    """

    # Initialize the LLM model
    model = _get_model()

    # Variable to hold the entire documentation text
    full_documentation_text = ""

    # Iterate over the files
    documentation = documentation.strip()
    messages = [
        {"role": "system", "content": prompt_2},
        {"role": "user", "content": prompt_user_2.format(documentation=documentation)}
    ]

    # Invoke the model to generate the doc based on the file description
    try:
        response = model.invoke(messages)
        full_documentation_text = response.content

    except Exception as e:
        print(f"Error generating documentation: {e}")

    #if  start with '```markdown' extract_code and return the content, else return the content
    if full_documentation_text.startswith('```markdown'):
        return extract_code(full_documentation_text, 'markdown')[0]
    return full_documentation_text
