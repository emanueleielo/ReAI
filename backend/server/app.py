from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os

from backend.agent.agent_ import start_agent
from backend.agent.loader import unzip_file

from backend.agent.loader import zip_project_folder


app = FastAPI()

# Configure CORS Middleware (if needed for cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your needs, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)




# Route for handling file uploads and streaming the state machine updates
@app.post("/process/")
async def upload_and_process(zip_file: UploadFile, tech_language: str = Form('Python'),
                             tech_framework: str = Form('FastAPI'), design_pattern: str = Form('Repository Pattern'),
                             other_requirements: str = Form(None)):
    """
    Endpoint to upload a .zip file, unzip it, and stream the state updates back to the client.

    Parameters:
    - zip_file: The uploaded zip file containing the folder structure.
    - tech_language, tech_framework, design_pattern, other_requirements: Additional input parameters.

    Returns:
    - StreamingResponse: A stream of updates, each update being the first key of the update dictionary.
    """
    # Create a temporary directory to unzip the file
    extract_path = "unzipped_folder"
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    # Save the uploaded zip file
    zip_file_location = f"temp_uploaded_{zip_file.filename}"
    with open(zip_file_location, "wb") as buffer:
        buffer.write(await zip_file.read())

    # Unzip the file
    unzip_file(zip_file_location, extract_path)

    # Prepare the input for the state machine (replace 'folder' with extracted folder path)
    input_data = {
        "folder_path": extract_path,  # This will replace 'folder'
        "tech_language": tech_language,
        "tech_framework": tech_framework,
        "design_pattern": design_pattern,
        "other_requirements": other_requirements
    }

    # Return a streaming response to the client
    return StreamingResponse(start_agent(input=input_data), media_type="text/plain")

@app.post("/download/")
async def download_project(folder_to_zip: str = Form('new_project')):
    """
    Endpoint to zip the 'new_project' folder and return it as a downloadable file.

    Returns:
    - StreamingResponse: The zipped folder as a downloadable file named 'new_project.zip'.
    """


    # Ensure the folder exists
    if not os.path.exists(folder_to_zip):
        return {"error": "The folder 'new_project' does not exist."}

    # Create the zipped file in memory
    zipped_file = zip_project_folder(folder_to_zip)

    # Return the zipped file as a StreamingResponse with the name 'new_project.zip'
    return StreamingResponse(zipped_file, media_type="application/x-zip-compressed",
                             headers={'Content-Disposition': 'attachment; filename=new_project.zip'})

#Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=0)