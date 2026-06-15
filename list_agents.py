import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv


# Force load the .env file
load_dotenv(override=True)


project_endpoint = os.getenv("PROJECT_ENDPOINT")


if not project_endpoint:
    print("❌ ERROR: PROJECT_ENDPOINT is missing from your environment configuration.")
    print("Please ensure your local .env file is set up correctly.")
    exit(1)


print("🔍 Authenticating and fetching agents from workspace project...")


try:
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()
    )


    agents = project_client.agents.list_agents()
    
    print("\n============================================================")
    print("              MANUTECH AI - REGISTERED AGENTS               ")
    print("============================================================")
    for agent in agents:
        # Excludes raw system prompt logic or routing keys
        print(f"👉 Name: {agent.name:<25} | ID: {agent.id}")
    print("============================================================\n")


except Exception as e:
    print(f"❌ Connection or Listing failed: {e}")


