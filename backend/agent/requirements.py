from .model import _get_model
from .state import AgentState

prompt = """You are tasked with generate a not technical requirements document, your document should describe in a really deep way all the feature of the project.
More detailed will be your documentation more easy will be for the user to understand the project.
Keep in mind that the user will use your description to generate a "technical requirement" document for a new system.

The input of the user will be a list of file and the description of each file.
You must be able from this input to give an high quality requirements document.
"""

prompt_user = """Files description:
<descriptions>
{DESCRIPTION}
</descriptions>
"""


def generate_requirements_(state: AgentState) -> str:
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": prompt_user.format(DESCRIPTION=state.get('file_descriptions'))}
    ]
    model = _get_model()
    response = model.invoke(messages)
    return response.content


prompt_tech = """You are tasked with generate a high technical requirements document, your document should describe in a really deep way all the feature of the project.
Keep in mind that an Agent LLM will use your description as a input to generate code for a whole project.
IS REALLY IMPORTANT THAT YOU GIVE A REALLY GOOD DESCRIPTION OF THE PROJECT, DESCRIBE EVERY ASPECT ON HOW THE CODE SHOULD BE AND GIVE SPECIFIC TASK AND GOAL TO EACH.

You must use a specific language and framework for this task.

LANGUAGE: {TECH_LANGUAGE}
FRAMEWORK: {TECH_FRAMEWORK}
DESIGN PATTERN: {DESIGN_PATTERN}
OTHER TECNHICAL REQUIREMENTS (if not provided, you can image it): {OTHER_REQUIREMENTS}
"""

prompt_user_tech = """Requirements of the project:
<requirements>
{REQUIREMENTS}
</requirements>
"""


def generate_tech_requirements_(state: AgentState) -> str:
    messages = [
        {"role": "system", "content": prompt_tech.format(TECH_LANGUAGE=state.get('input').get('tech_language'),
                                                            DESIGN_PATTERN=state.get('input').get('design_pattern'),
                                                         OTHER_REQUIREMENTS=state.get('input').get('other_requirements'),
                                                         TECH_FRAMEWORK=state.get('input').get('tech_framework'))},
        {"role": "user", "content": prompt_user.format(DESCRIPTION=state.get('file_descriptions'))}
    ]
    model = _get_model()
    response = model.invoke(messages)
    return response.content
