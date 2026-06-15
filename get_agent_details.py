import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv('PROJECT_ENDPOINT', 'https://manutech-ai-resource.services.ai.azure.com/api/projects/manutech-ai')
agent_name = os.getenv('AGENT_ID', 'ManuTech-Ai')
print('Using endpoint:', endpoint)
print('Agent name:', agent_name)

client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
try:
    agent = client.agents.get(agent_name)
    import json
    # Print a few fields
    d = {}
    for k in ('name','id','versions'):
        d[k] = getattr(agent, k, None)
    print('Agent top-level fields:')
    print(json.dumps(d, indent=2, default=str))
    # Print full object repr for inspection
    print('\nFull agent object:')
    print(agent)
except Exception as e:
    print('Error fetching agent:', type(e), e)
    try:
        resp = getattr(e, 'response', None)
        if resp is not None:
            print('HTTP status:', getattr(resp, 'status', None))
            try:
                print('Response text:', resp.text)
            except Exception:
                pass
    except Exception as e2:
        print('Error inspecting exception:', e2)
    raise
