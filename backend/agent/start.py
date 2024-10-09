import json
import re
import os
from agent.model import _get_model
from agent.state import AgentState

prompt = """You are tasked understand how to startup an application and write a documentation about it.
The user will give you some information about the project and the code and you must understand how to use it.
Your output should be .md documentation that describe how to start the app (eg. how to run the tests, how to start the app, etc).


tech language: {TECH_LANGUAGE}
tech framework: {TECH_FRAMEWORK}
"""


prompt_user = """This is are some of information that you can have about the app.
<code>
{CODE}
</code>
"""
def write_startup(state: AgentState, files, base_path='new_project') -> str:
    """
    Generate doc based on the files description. File is a list of dictionaries with the following keys: full_path, file_description, code, documentation.

    :param state: Contains the current agent's state, including file descriptions.
    :param files: A list of dictionaries, each containing 'full_path' and 'file_description', 'code', 'documentation'.
    :return: The list of files with the generated code written to them.
    """

    # Initialize the LLM model
    model = _get_model()
    files_str = json.dumps(files)
    messages = [
            {"role": "system", "content": prompt.format(TECH_LANGUAGE=state.get('input').get('tech_language'), TECH_FRAMEWORK=state.get('input').get('tech_framework'))},
            {"role": "user", "content": prompt_user.format(CODE=files_str)}
        ]

    response = model.invoke(messages)

    full_path = os.path.join(base_path, 'start.md')
    # Write the generated code to the file
    with open(full_path, 'w') as f:
        f.write(response.content)

    return 'The new project has been created, go into the new_project folder to see the start.md file'

