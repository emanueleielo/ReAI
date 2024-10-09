import os

from backend.agent.loader import load_github_file, load_pdf_file, read_file_content
from backend.agent.model import _get_model
from backend.agent.state import AgentState



prompt = """You are tasked with reading, understanding and then generating a description legacy code.
Keep in mind that the user will use your description to generate a "requirements" document for a new system.

When you generate description you should follow this format:
_______
FILE NAME : [FILE_NAME] <- Name of the file
CORE UTILITY [CORE_UTILITY] <- This is the main use case of the file that you are analyzing
TECHNICAL ANALYSIS [TECHNICAL_ANALYSIS] <- This is the technical analysis of the file, describe the methods, classes, functions, etc.
_______
"""

prompt_user = """Analyze this code:
<code_to_analyze>
{CODE}
</code_to_analyze>
"""

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

VALID_FILE_EXTENSIONS = ['.py', '.md', '.html', '.txt', '.js', '.css', '.json',
                         '.xml', '.yml', '.yaml', '.sh', '.cob', '.c', '.cpp', '.java', '.cs', '.php', '.rb', '.pl', '.sql',
                         '.swift', '.kt', '.go', '.ts', '.r', '.m', '.jl', '.hs', '.fs', '.fsx', '.fsi', '.clj',
                         '.cljs', '.cljc', '.edn', '.ex', '.exs', '.erl', '.hrl', '.lua', '.ml', '.mli', '.mll', '.mly',
                         '.pas', '.dpr', '.dproj', '.lpr', '.lfm', '.lpi', '.lps', '.lfs', 'Dockerfile']


def describe_files_in_folder(state: AgentState | str, file_descriptions: str = "") -> str:
    """
    Recursively processes valid files in a folder and its subfolders,
    excluding specific common project folders, and generates file descriptions.

    Parameters:
    state (AgentState | str): The state object containing the folder path or the folder path as a string.
    file_descriptions (str): The accumulated file descriptions.

    Raises:
    FileNotFoundError: If the folder path does not exist.
    """
    try:
        if isinstance(state, dict):
            folder_path = state.get('input')['folder_path']
        else:
            folder_path = state
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

        with os.scandir(folder_path) as entries:
            for entry in entries:
                # Skip folders in the exclusion list
                if entry.is_dir() and entry.name in EXCLUDED_FOLDERS:
                    continue

                # If the entry is a file, process it if it has a valid extension
                if entry.is_file() and any(entry.name.endswith(ext) for ext in VALID_FILE_EXTENSIONS):
                    file_path = entry.path
                    file_content = read_file_content(file_path)
                    file_description = get_file_description(file_content)
                    # Append the description to the accumulated variable
                    file_descriptions += f"Description for {entry.name}:\n{file_description}\n\n"

                # If the entry is a directory, recursively process its contents
                if entry.is_dir():
                    file_descriptions = describe_files_in_folder(entry.path, file_descriptions)
        return file_descriptions

    except FileNotFoundError as e:
        print(str(e))


def get_file_description(file_content: str) -> str:

    messages = [
        {"role": "system", "content": prompt},
                   {"role": "user", "content": prompt_user.format(CODE=file_content)}
    ]
    model = _get_model()
    response = model.invoke(messages)
    return response.content
