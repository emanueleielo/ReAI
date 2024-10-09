import re

from agent.model import _get_model
from agent.state import AgentState
from agent.utils import extract_code

prompt = """You are tasked to generate a folder structure based on a technical document.
The user will provide you a specific document with the requirements of the project, from this you must extract a struture folder.
The structure folder that you will create will be used by the User to start the creation of each file/folders of the project.

For each file the important information about it are:
file_name: The name of the file
file_description: The description of the file, this should contain all the methods and classes that the file contains with all the documentation and description about them,
this description must be HIGH accurate because an LLM will use this information to generate the code that MUST work and should be well connected with the rest of the project and other files.

The structure must be written in JSON format. AND YOU MUST ANSWER ONLY IN JSON FORMAT.
<structure_json>
{
  "root": {
    "FolderA": {
      "SubFolderA1": {
        "SubSubFolderA1": [
          {
            "file_name": "file1.txt",
            "file_description": "Text file in SubSubFolderA1"
          },
          {
            "file_name": "file2.py",
            "file_description": "Python file in SubSubFolderA1"
          }
        ]
      },
      "SubFolderA2": {
        "SubSubFolderA2": {
          "SubSubSubFolderA1": [
            {
              "file_name": "file3.md",
              "file_description": "Markdown file in SubSubSubFolderA1"
            }
          ]
        },
        "files": [
          {
            "file_name": "file4.html",
            "file_description": "HTML file in SubFolderA2"
          }
        ]
      },
      "files": [
        {
          "file_name": "file5.js",
          "file_description": "JavaScript file in FolderA"
        }
      ]
    },
    "FolderB": {
      "SubFolderB1": {
        "SubSubFolderB1": [
          {
            "file_name": "file6.css",
            "file_description": "CSS file in SubSubFolderB1"
          },
          {
            "file_name": "file7.json",
            "file_description": "JSON file in SubSubFolderB1"
          }
        ],
        "SubSubFolderB2": [
          {
            "file_name": "file8.txt",
            "file_description": "Text file in SubSubFolderB2"
          }
        ]
      },
      "files": [
        {
          "file_name": "file9.js",
          "file_description": "JavaScript file in FolderB"
        }
      ]
    },
    "files": [
      {
        "file_name": "file10.yml",
        "file_description": "YAML configuration file in root"
      }
    ]
  }
}
</structure_json>
IMPORTANT: REMEMBER TO ANSWER ONLY WITH THE JSON, DO NOT ADD ANY OTHER INFORMATION.
IMPORTANT: REMEMBER THE DESCRIPTION MUST BE ACCURATE.


EXAMPLE
```json
...
```
"""

prompt_user = """Requirements of the project:
<requirements>
{REQUIREMENTS}
</requirements>

Technical requirements:
<tech_requirements>
{TECH_REQUIREMENTS}
</tech_requirements>

Tech language: <tech_language>{TECH_LANGUAGE}</tech_language>
Tech framework: <tech_framework>{TECH_FRAMEWORK}</tech_framework>
"""


def pretty_print_folder_structure(folder_structure, prefix=""):
    """
    Recursively generates a tree-like structure from the given JSON structure and returns it as a string.

    :param folder_structure: The folder structure in dictionary format.
    :param prefix: The current prefix (used for indentation).
    :return: The tree-like structure as a string.
    """
    result = ""

    for key, value in folder_structure.items():
        # Se è un dizionario, è una cartella
        if isinstance(value, dict):
            if key == "files":
                # Se la chiave è "files", ignora la cartella "files" e gestisci direttamente i file
                result += pretty_print_folder_structure(value, prefix)
            else:
                result += f"{prefix}└── {key}/\n"
                result += pretty_print_folder_structure(value, prefix + "    ")
        elif isinstance(value, list):
            # Se è una lista, sono file dentro la cartella
            for i, file in enumerate(value):
                if isinstance(file, dict) and 'file_name' in file:
                    is_last_file = i == len(value) - 1
                    connector = "└── " if is_last_file else "├── "
                    result += f"{prefix}{connector}{file['file_name']}\n"
                elif isinstance(file, str):
                    result += f"{prefix}└── {file}\n"

    return result

def generate_new_structure(state: AgentState) -> str:
    requirements = state.get('requirements')
    tech_requirements = state.get('technical_requirements')
    tech_language = state.get('input').get('tech_language')
    tech_framework = state.get('input').get('tech_framework')
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": prompt_user.format(REQUIREMENTS=requirements,TECH_REQUIREMENTS=tech_requirements, TECH_LANGUAGE=tech_language,
                                                       TECH_FRAMEWORK=tech_framework)}
    ]
    model = _get_model()
    response = model.invoke(messages)
    content = response.content
    #if response content start with '```json' and end with '```' then return the content

    return extract_code(content, 'json')[0]
