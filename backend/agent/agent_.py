import os

from langgraph.graph import Graph, MessagesState, StateGraph

from agent.documentation import write_documentation, rewrite_documentation
from agent.generate_structure import create_files_and_folders
from agent.new_structure import generate_new_structure, pretty_print_folder_structure
from agent.old_structure import create_folder_structure_text
from agent.read import describe_files_in_folder
from agent.requirements import generate_requirements_, generate_tech_requirements_
from agent.sequence_diagram import generate_diagram
from agent.start import write_startup
from agent.state import OutputState, AgentState, InputState
from agent.utils import write_file

from agent.write_code import write_code

import logging



# Define the nodes
def start(input_: InputState) -> dict:
    logging.info("Starting the process")
    logging.info(input_.get('The folder path is: ' + 'folder_path'))
    return {"input": input_}


def create_folder_structure(state: AgentState) -> dict:
    """
    Create a folder structure (text) based on the project
    :param state:
    :return:
    """
    logging.info("Creating the folder structure")
    structure: str = create_folder_structure_text(state.get('input')['folder_path'])
    # Logic to create a folder structure based on the project
    return {"old_structure": structure}


def read_files(state: AgentState) -> dict:
    """
    Read the files in the folder, for each file generate a description and add it in the state.
    :param state:
    :return:
    """
    file_descriptions = describe_files_in_folder(state)
    return {"file_descriptions": file_descriptions}


def generate_requirements(state: AgentState) -> dict:
    """
    Reading the file_descriptions,
    generate a list of requirements for the project,
    that should be not technical and only describe the features of the project.

    :param state:
    :return:
    """
    requirements = generate_requirements_(state)
    return {"requirements": requirements}


def generate_technical_requirements(state: AgentState) -> dict:
    """
    Reading the file_descriptions, generate a list of technical requirements for the project.
    :param state:
    :return:
    """
    # Logic to generate technical requirements for a specific tech stack
    requirements_tech = generate_tech_requirements_(state)
    return {"technical_requirements": requirements_tech}


def generate_architecture_diagram(state: AgentState) -> dict:
    """
    Generate an architecture diagram based on the technical requirements.
    :param state:
    :return:
    """
    diagram = generate_diagram(state)
    return {"architecture_diagram": diagram}


def generate_folder_file_structure(state: AgentState) -> dict:
    """
    Generate a folder and file structure based on the architecture diagram.
    :param state:
    :return:
    """
    import json
    new_structure = generate_new_structure(state)
    new_structure_json = json.loads(new_structure)

    pretty_structure: str = pretty_print_folder_structure(new_structure_json)
    return {"new_structure": new_structure_json, "new_structure_pretty": pretty_structure}


def generate_files(state: AgentState) -> dict:
    """
    Generate files,  based on the new structure
    :param state:
    :return:
    """
    generated_files = create_files_and_folders(state.get('new_structure'))
    generated_files = write_code(state, generated_files)
    documentation = write_documentation(state, generated_files)
    rewritten_documentation = rewrite_documentation(documentation)
    write_file('new_project/documentation.md', rewritten_documentation)
    return {"generated_files": generated_files}


def start_application_and_test(state: AgentState) -> dict:
    # Logic to start the application and test with a curl
    output = write_startup(state, state.get('generated_files'))

    return {"output": output}


# Create the graph

graph = StateGraph(AgentState, input=InputState, output=OutputState)

# Add nodes to the graph
graph.add_node("start", start)
graph.add_node("create_folder_structure", create_folder_structure)
graph.add_node("read_files", read_files)
graph.add_node("generate_requirements", generate_requirements)
graph.add_node("generate_technical_requirements", generate_technical_requirements)
graph.add_node("generate_architecture_diagram", generate_architecture_diagram)
graph.add_node("generate_folder_file_structure", generate_folder_file_structure)
graph.add_node("generate_files", generate_files)
graph.add_node("start_application_and_test", start_application_and_test)

# Define the edges
graph.set_entry_point('start')
graph.add_edge('start', 'create_folder_structure')
graph.add_edge("create_folder_structure", "read_files")
graph.add_edge("read_files", "generate_requirements")
graph.add_edge("generate_requirements", "generate_technical_requirements")
graph.add_edge("generate_technical_requirements", "generate_architecture_diagram")
graph.add_edge("generate_architecture_diagram", "generate_folder_file_structure")
graph.add_edge("generate_folder_file_structure", "generate_files")
graph.add_edge("generate_files", "start_application_and_test")
graph.set_finish_point("start_application_and_test")

# Compile the graph
app = graph.compile()


async def start_agent(input: dict):
    async for update in app.astream(input=input, stream_mode="updates"):
        #first key of dict
        node = list(update.keys())[0]
        print(update)
        yield '<node>' + node + '</node>'
