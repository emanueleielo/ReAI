import functools
from functools import lru_cache
import time
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import os

import io

CACHE_DURATION = 24 * 60 * 60

import zipfile


def read_file_content(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a string.

    Parameters:
    file_path (str): The full path of the file to read.

    Returns:
    str: The content of the file as a string.

    Raises:
    FileNotFoundError: If the provided file path is invalid.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: The file '{file_path}' does not exist."


def unzip_file(zip_path: str, extract_to: str) -> None:
    """
    Unzips the given .zip file to the specified directory.

    Parameters:
    zip_path (str): The full path of the zip file to unzip.
    extract_to (str): The directory where the zip file should be extracted.

    Raises:
    FileNotFoundError: If the provided zip_path is invalid.
    zipfile.BadZipFile: If the provided file is not a valid zip file.
    """
    try:
        # Check if the provided file path is a valid zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all contents of the zip file to the target directory
            zip_ref.extractall(extract_to)
            print(f"Successfully extracted {zip_path} to {extract_to}")
    except FileNotFoundError:
        print(f"Error: The file '{zip_path}' does not exist.")
    except zipfile.BadZipFile:
        print(f"Error: The file '{zip_path}' is not a valid zip file.")


def time_based_cache(seconds):
    def wrapper_cache(func):
        func = lru_cache(maxsize=None)(func)
        func.lifetime = seconds
        func.expiration = time.time() + func.lifetime

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


@time_based_cache(CACHE_DURATION)
def load_github_file(url):
    # Convert GitHub URL to raw content URL
    raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    # Send a GET request to the raw URL
    response = requests.get(raw_url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to load file. Status code: {response.status_code}"


@time_based_cache(CACHE_DURATION)
def load_pdf_file(url):
    # Scaricare il PDF dal URL
    response = requests.get(url)
    if response.status_code == 200:
        # Caricare il PDF in memoria
        pdf_file = BytesIO(response.content)

        # Leggere il PDF con PyPDF2
        reader = PdfReader(pdf_file)

        # Estrarre il testo da tutte le pagine
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()

        # Stampare o usare il testo estratto
        print(extracted_text)
    else:
        print(f"Errore nel download del PDF. Status code: {response.status_code}")


def zip_project_folder(folder_path: str) -> io.BytesIO:
    """
    Zips the contents of the folder and returns it as a BytesIO object.
    The name of the zip file will be the same as the folder name being zipped.

    :param folder_path: Path to the folder to zip.
    :return: A BytesIO object of the zipped folder.
    """
    # Controlla se la cartella esiste, altrimenti lancia un'eccezione
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")

    memory_file = io.BytesIO()

    folder_name = os.path.basename(os.path.normpath(folder_path))  # Get the folder name
    zip_file_name = f"{folder_name}.zip"  # Name the zip file based on the folder name

    # Crea il file zip
    with zipfile.ZipFile(memory_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))  # Use relative paths

    memory_file.seek(0)  # Reset the buffer position to the beginning

    return memory_file
