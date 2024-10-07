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
    input:InputState
    old_structure: str
    file_descriptions: str
    requirements: str
    technical_requirements: str
    architecture_diagram: str
    new_structure: dict
    generated_files: list
    unit_tests: list
    documentation: list


class OutputState(MessagesState):
    output: str


class GraphConfig(TypedDict):
    gather_model: Literal['openai', 'anthropic']
    draft_model: Literal['openai', 'anthropic']
    critique_model: Literal['openai', 'anthropic']
