
from .model import _get_model
from .state import AgentState
import os

prompt = """You are tasked to generate a folder structure based on a technical document.
The user will provide you a specific document with the requirements of the project, from this you must extract a struture folder.
The structure folder that you will create will be used by the User to start the creation of each file/folders of the project.

The structure must be written in Mermaid Language. AND YOU MUST ANSWER ONLY IN Mermaid Language.
<structure>
sequenceDiagram
    participant web as Web Browser
    participant blog as Blog Service
    participant account as Account Service
    participant mail as Mail Service
    participant db as Storage

    Note over web,db: The user must be logged in to submit blog posts
    web->>+account: Logs in using credentials
    account->>db: Query stored accounts
    db->>account: Respond with query result

    alt Credentials not found
        account->>web: Invalid credentials
    else Credentials found
        account->>-web: Successfully logged in

        Note over web,db: When the user is authenticated, they can now submit new posts
        web->>+blog: Submit new post
        blog->>db: Store post data

        par Notifications
            blog--)mail: Send mail to blog subscribers
            blog--)db: Store in-site notifications
        and Response
            blog-->>-web: Successfully posted
        end
    end
</diagram_example>

"""


prompt_user = """Requirements of the project:
<requirements>
{REQUIREMENTS}
</requirements>
"""
def generate_diagram(state: AgentState, base_path = 'new_project') -> str:

    messages = [
        {"role": "system", "content": prompt},
                   {"role": "user", "content": prompt_user.format(REQUIREMENTS=state.get('file_descriptions'))}
    ]
    model = _get_model()
    response = model.invoke(messages)

    os.makedirs(base_path, exist_ok=True)

    full_path = os.path.join(base_path, 'architecture.md')
    # Write the generated code to the file
    with open(full_path, 'w') as f:
        f.write(response.content)
    return response.content

