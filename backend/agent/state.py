from langgraph.graph import MessagesState
from typing import TypedDict, Literal
# Define the state for the graph

class InputState(MessagesState):
    folder_path: str
    tech_language: str
    tech_framework:str
    design_pattern: str
    other_requirements: str


class AgentState(MessagesState):
    input:InputState # This is the input that will come from the user (FastAPI endpoint)
    old_structure: str # This is the old structure of the project
    file_descriptions: str # This is the description of the files in the project (old files that are analyzed)
    requirements: str # This is the requirements of the project (non-technical)
    technical_requirements: str # This is the technical requirements of the project
    architecture_diagram: str # This is the architecture diagram of the project (mermaid language)
    new_structure: dict # This is the new structure of the project
    new_structure_pretty: str # This is the new structure of the project in a pretty format
    generated_files: list # This is the list of files that were generated
    unit_tests: list # This is the unit tests that were generated
    documentation: list # This is the documentation that was generated


class OutputState(MessagesState):
    output: str


class GraphConfig(TypedDict):
    gather_model: Literal['openai', 'anthropic']
    draft_model: Literal['openai', 'anthropic']
    critique_model: Literal['openai', 'anthropic']
