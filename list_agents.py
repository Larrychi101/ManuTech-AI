import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

# Load your endpoint from .env
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT", "https://manutech-ai-resource.services.ai.azure.com/api/projects/manutech-ai")
# If the provided endpoint accidentally points to an agent-specific OpenAI URL,
# trim it back to the project-level endpoint (everything before '/agents/').
if "/agents/" in project_endpoint:
    project_endpoint = project_endpoint.split("/agents/")[0]
print('Using project endpoint:', project_endpoint)

# Initialize the client
with AIProjectClient(
    endpoint=project_endpoint, 
    credential=DefaultAzureCredential()
) as project_client:
    
    print("🔍 Fetching agents from your project...")
    # List all agents associated with this project
    agents = project_client.agents.list()

    # Iterate and print details (paged result)
    try:
        for agent in agents:
            # Agent model may expose 'name' or 'identifier'
            name = getattr(agent, 'name', None) or getattr(agent, 'identifier', None) or getattr(agent, 'id', None)
            print(f"Name: {name}")
    except Exception as e:
        print('Error while iterating agents:', type(e), e)
        # Try to surface HTTP response details when available
        try:
            resp = getattr(e, 'response', None)
            if resp is not None:
                print('HTTP status:', getattr(resp, 'status', None))
                try:
                    print('Response text:', resp.text)
                except Exception:
                    pass
        except Exception as e2:
            print('Error inspecting exception response:', e2)
        raise
