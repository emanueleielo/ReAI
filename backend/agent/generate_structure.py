
import os

from .read import VALID_FILE_EXTENSIONS




import os


def create_files_and_folders(structure: dict, base_path='new_project') -> list[dict]:
    """
    Recursively creates files and folders based on the given structure.

    Parameters:
    structure (dict): A dictionary representing the folder and file structure.
    base_path (str): The base path where the project structure will be created.

    Returns:
    list: A list of dictionaries where each dictionary contains the full path of the created files.
    """
    created_files = []  # To store the created files

    # If the base path does not exist, create it
    os.makedirs(base_path, exist_ok=True)

    # Iterate over the structure
    for key, value in structure.items():
        current_path = os.path.join(base_path, key)

        # If the value is a dictionary, it may contain 'files' and/or subdirectories
        if isinstance(value, dict):
            # First, handle 'files' if present
            if 'files' in value and isinstance(value['files'], list):
                for file_info in value['files']:
                    file_name = file_info['file_name']
                    file_description = file_info.get('file_description', 'No description provided')

                    # Construct the full file path
                    file_path = os.path.join(current_path, file_name)

                    try:
                        # Ensure the directory for the file exists
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)

                        # Create the file with the description as a comment
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(f"# {file_description}\n")
                        print(f"Created file: {file_path}")

                        # Add the file to the list of created files
                        created_files.append({
                            "file_name": file_name,
                            "full_path": file_path,
                            "file_description": file_description
                        })
                    except OSError as e:
                        print(f"Error creating file {file_path}: {e}")

            # Then, handle subdirectories
            for sub_key, sub_value in value.items():
                if sub_key != 'files' and isinstance(sub_value, dict):
                    # Create the subdirectory
                    os.makedirs(os.path.join(current_path, sub_key), exist_ok=True)
                    print(f"Created folder: {os.path.join(current_path, sub_key)}")

                    # Recursively process the subdirectory
                    created_files.extend(create_files_and_folders({sub_key: sub_value}, current_path))

        else:
            print(f"Unexpected structure for key '{key}': Expected dict, got {type(value)}")

    return created_files