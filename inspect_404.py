from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os
import traceback

endpoint = os.getenv('PROJECT_ENDPOINT', 'https://manutech-ai-resource.services.ai.azure.com/api/projects/manutech-ai')
agent_id = os.getenv('AGENT_ID', 'ManuTech-Ai')
print('Project endpoint:', endpoint)
print('Agent id:', agent_id)

client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential(), allow_preview=True)
openai_client = client.get_openai_client(agent_name=agent_id)
# Try to access base_url attribute
base_url = getattr(openai_client, 'base_url', None) or getattr(openai_client, '_base_url', None)
print('OpenAI client base_url:', base_url)

try:
    print('\nAttempting a lightweight responses.create call...')
    resp = openai_client.responses.create(input='hello')
    print('Response:', resp)
except Exception as e:
    print('Exception type:', type(e))
    print('Exception:', e)
    try:
        if hasattr(e, 'response') and e.response is not None:
            r = e.response
            print('HTTP status:', getattr(r, 'status', None))
            try:
                print('Response text:', r.text)
            except Exception:
                pass
            try:
                req = getattr(r, 'request', None)
                if req is not None:
                    print('Request url:', getattr(req, 'url', None))
            except Exception:
                pass
    except Exception as e2:
        print('Error while inspecting exception:', e2)
    traceback.print_exc()
