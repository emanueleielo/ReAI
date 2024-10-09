import re
import os
from .model import _get_model
from .state import AgentState
from .utils import extract_code
from concurrent.futures import ThreadPoolExecutor, as_completed

prompt = """You are tasked to generate code as the user request.
The code that you must write must be contextualized, because this code belong to a big project and must work in relation with other file.
The user will give you some information about the project to better contextualize and help you on the task.
Remember to document and comment well the code that you generate.

IMPORTANT: You need to be consistent with the rest of the project and the import that you do in the code.
For this reason the user will give you the structure of the project so you must be accurate with the import that you do in the code.

PRETTY VIEW OF THE PROJECT STRUCTURE:
{PROJECT_STRUCTURE}

TECH LANGUAGE: {TECH_LANGUAGE}
TECH FRAMEWORK: {TECH_FRAMEWORK}

<requirements>
{REQUIREMENTS}
</requirements>

<tech_requirements>
{TECH_REQUIREMENTS}
</tech_requirements>


You generate code using markdown {TECH_LANGUAGE} syntax, eg:

```{TECH_LANGUAGE}
...
```

IMPORTANT: Remember, only generate one of those code blocks!"
"""

prompt_user = """This is the description of the files that you must generate code for:
<code_file_name>
{CODE_FULL_PATH}
</code_file_name>
<code_description>
{CODE_DESCRIPTION}
</code_description>
"""



def write_code(state: AgentState, files) -> str:
    """
    Generate code based on the files description in a multi-threaded way.
    Each file is processed on a separate thread, and the code is written to its respective file path.

    :param state: Contains the current agent's state, including file descriptions.
    :param files: A list of dictionaries, each containing 'full_path' and 'file_description'.
    :return: The list of files with the generated code written to them.
    """

    # Initialize the LLM model
    model = _get_model()

    def process_file(file):
        full_path = file['full_path']
        file_description = file['file_description']

        # Prepare the LLM prompt for generating code
        messages = [
            {"role": "system", "content": prompt.format(TECH_LANGUAGE=state.get('input').get('tech_language'),
                                                        TECH_FRAMEWORK=state.get('input').get('tech_framework'),
                                                        REQUIREMENTS=state.get('requirements'),
                                                        PROJECT_STRUCTURE=state.get('new_structure_pretty'),
                                                        TECH_REQUIREMENTS=state.get('technical_requirements'))},
            {"role": "user",
             "content": prompt_user.format(CODE_DESCRIPTION=file_description, CODE_FULL_PATH=full_path)}
        ]

        try:
            # Invoke the model to generate the code based on the file description
            response = model.invoke(messages)

            # if response starts with ```tech_language, extract the code or use response.content
            if response.content.startswith(f"```{state.get('input').get('tech_language')}"):
                generated_code = extract_code(response.content, state.get('input').get('tech_language'))[0]
            else:
                generated_code = response.content

            file['code'] = generated_code

            # Ensure the directory exists before writing the file
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Write the generated code to the file
            with open(full_path, 'w') as f:
                f.write(generated_code)

            print(f"Code written to {full_path}")

        except Exception as e:
            # Log the error but continue
            print(f"Error generating or writing code for {full_path}: {e}")
            file['code'] = None  # You might want to track files that failed

        return file

    # Use ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor() as executor:
        # Submit each file for processing in a separate thread
        futures = {executor.submit(process_file, file): file for file in files}

        # Wait for all threads to complete and collect the results
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions caught during processing

    return files