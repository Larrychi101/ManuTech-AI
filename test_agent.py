import os
from dotenv import load_dotenv  # Run 'pip install python-dotenv' first
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()  # This loads your secrets from the .env file

project_endpoint = os.getenv("PROJECT_ENDPOINT", "https://manutech-ai-resource.services.ai.azure.com/api/projects/manutech-ai")
agent_id = os.getenv("AGENT_ID", "Manutech-Ai")

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)
openai_client = project_client.get_openai_client(agent_name=agent_id)

print(f"Using project endpoint: {project_endpoint}")
print(f"Using agent id: {agent_id}")

while True:
    try:
        user_input = input("\nYou: ")
    except EOFError:
        break
    if user_input.lower() == "exit":
        break

    try:
        response = openai_client.responses.create(input=user_input)
    except Exception as e:
        print(f"❌ Request failed: {e}")
        continue

    # The response content may be nested; fallback to printing the raw response if needed.
    assistant_text = None
    if hasattr(response, "output") and response.output:
        first_output = response.output[0]
        if hasattr(first_output, "content") and first_output.content:
            assistant_text = getattr(first_output.content[0], "text", None)
    if assistant_text is None:
        assistant_text = str(response)

    print(f"ManuTech AI: {assistant_text}")


import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

# Force load the .env file
load_dotenv(override=True)

project_endpoint = os.getenv("PROJECT_ENDPOINT")

# Debugging: Print what the script sees
print(f"DEBUG: Found Endpoint: {project_endpoint}")

if not project_endpoint:
    print("❌ ERROR: PROJECT_ENDPOINT is None! Check your .env file or hardcode the URL in the script.")
    exit(1)

# Initialize the client
try:
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()
    )

    print("🔍 Fetching agents from your project...")
    agents = project_client.agents.list_agents()
   
    for agent in agents:
        print(f"Name: {agent.name}, ID: {agent.id}")

except Exception as e:
    print(f"❌ Connection failed: {e}")
