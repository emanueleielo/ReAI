import os


# List of common folder names to exclude (e.g., project dependency folders, virtual environments, etc.)
EXCLUDED_FOLDERS = [
    'node_modules',  # JavaScript/Node.js dependencies
    '.venv',         # Python virtual environments
    '.git',          # Git version control folder
    '__pycache__',   # Python cache folder
    'dist',          # Common distribution folder for built files
    'build',         # Common build folder
    '.idea',         # IntelliJ project files
    '.vscode',       # Visual Studio Code settings
    'env',           # Another common virtual environment folder
    '.DS_Store',     # MacOS specific metadata file
    'coverage',      # Code coverage reports folder
]


def create_folder_structure_text(folder_path: str, prefix: str = "") -> str:
    """
    Recursively generates a tree-like structure of the folder's content,
    excluding specific common project folders like 'node_modules', '.venv', '.git', etc.

    Parameters:
    folder_path (str): The path to the folder to describe.
    prefix (str): A string used to format the tree structure for each folder level.

    Returns:
    str: A tree-like text representation of the folder and its files.

    Raises:
    FileNotFoundError: If the folder path does not exist.
    """
    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

        result = ""
        with os.scandir(folder_path) as entries:
            entries = sorted(entries, key=lambda e: e.is_file())  # Sort directories before files
            num_entries = len(entries)
            for index, entry in enumerate(entries):
                # Skip folders in the exclusion list
                if entry.is_dir() and entry.name in EXCLUDED_FOLDERS:
                    continue

                # Determine whether this is the last entry in the current directory
                is_last = index == (num_entries - 1)

                # Format the entry with tree-like structure
                connector = "└── " if is_last else "├── "
                result += f"{prefix}{connector}{entry.name}/\n" if entry.is_dir() else f"{prefix}{connector}{entry.name}\n"

                # If the entry is a directory, recursively list its contents
                if entry.is_dir():
                    child_prefix = "    " if is_last else "│   "
                    result += create_folder_structure_text(entry.path, prefix + child_prefix)

        return result

    except FileNotFoundError as e:
        return str(e)
