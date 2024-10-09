import os

from backend.agent.old_structure import EXCLUDED_FOLDERS
from backend.agent.read import VALID_FILE_EXTENSIONS


def create_files_and_folders(structure: dict, base_path='new_project') -> list:
    """
    Recursively creates files and folders based on the given structure.

    Parameters:
    structure (dict): A dictionary representing the folder and file structure.
    base_path (str): The base path where the project structure will be created.

    Returns:
    list: A list of dictionaries where each dictionary contains the full path of the created files.
    """

    # List to store the created files and their full paths
    created_files = []

    # If the base path does not exist, create it
    os.makedirs(base_path, exist_ok=True)

    # Iterate over the dictionary structure
    for key, value in structure.items():
        # Construct the current path based on the base path and the current folder
        current_path = os.path.join(base_path, key)

        # If the value is a list or the value is str and finish with VALID_FILE_EXTENSIONS, it represents files inside the current directory
        if isinstance(value, list) or (isinstance(value, str) and value.endswith(tuple(VALID_FILE_EXTENSIONS))) or (
                isinstance(value, dict) and 'files' in value and isinstance(value['files'], list)):          # Process the files directly in the current folder (base_path)
            for file_info in value:
                if isinstance(file_info, dict):  # Ensure it's a dictionary representing a file
                    file_name = file_info['file_name']
                    file_description = file_info['file_description']

                    # Construct the full file path
                    file_path = os.path.join(base_path, file_name)

                    # Create an empty file
                    with open(file_path, 'w') as f:
                        f.write("")  # Ignore the description for now
                    print(f"Created file: {file_path}")

                    # Add the created file to the list as a dictionary with its full path
                    created_files.append({
                        "file_name": file_name,
                        "full_path": file_path,
                        'file_description': file_description
                    })

        elif isinstance(value, dict):
            # If it's a dictionary (subfolder), create the folder and process its contents
            os.makedirs(current_path, exist_ok=True)
            print(f"Created folder: {current_path}")
            # Recursively process the contents of the folder
            created_files.extend(create_files_and_folders(value, current_path))

    # Return the list of created files
    return created_files