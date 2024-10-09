import re
import os
from agent.model import _get_model
from agent.state import AgentState
from agent.utils import extract_code

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
    Generate code based on the files description. File is a list of dictionaries with the following keys: full_path, file_description.
    For each file, we invoke `model.invoke` to generate the code with the LLM.
    Once we have the code as a string for each file, we take the full_path of the file and write the code on it.

    :param state: Contains the current agent's state, including file descriptions.
    :param files: A list of dictionaries, each containing 'full_path' and 'file_description'.
    :return: The list of files with the generated code written to them.
    """

    # Initialize the LLM model
    model = _get_model()

    # Iterate over the files
    for file in files:
        full_path = file['full_path']
        file_description = file['file_description']

        # Prepare the LLM prompt for generating code
        messages = [
            {"role": "system", "content": prompt.format(TECH_LANGUAGE=state.get('input').get('tech_language'),
                                                        TECH_FRAMEWORK=state.get('input').get('tech_framework'),
                                                        REQUIREMENTS=state.get('requirements'),
                                                        PROJECT_STRUCTURE=state.get('new_structure_pretty'),
                                                        TECH_REQUIREMENTS=state.get('technical_requirements'))},
            {"role": "user", "content": prompt_user.format(CODE_DESCRIPTION=file_description, CODE_FULL_PATH=full_path)}
        ]

        try:
            # Invoke the model to generate the code based on the file description
            response = model.invoke(messages)

            #if start with ```tech_language use extract_code to get the code or use the response.content
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
            # Log the error but continue with the next file
            print(f"Error generating or writing code for {full_path}: {e}")
            continue  # Skip to the next file

    return files