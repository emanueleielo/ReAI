import re

import dotenv
import os

dotenv.load_dotenv()


# Load environment variables
def get_env(key, default=None):
    return os.getenv(key, default)




def extract_code(text, lang):
    """
    Extract code blocks from the text based on the provided language.

    Parameters:
    text (str): The text containing code blocks.
    lang (str): The language to match (e.g., 'python', 'javascript').

    Returns:
    list: A list of extracted code blocks.
    """
    pattern = rf'```{lang}\s*(.*?)\s*(```|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match[0] for match in matches]


def write_file(full_path, content):
    """
    Write content to a file.

    Parameters:
    full_path (str): The full path of the file to write to.
    content (str): The content to write to the file.
    """
    with open(full_path, 'w') as f:
        f.write(content)