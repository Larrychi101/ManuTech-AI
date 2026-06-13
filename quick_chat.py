import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
endpoint = os.getenv('PROJECT_ENDPOINT', 'https://manutech-ai-resource.services.ai.azure.com/api/projects/manutech-ai')
agent_id = os.getenv('AGENT_ID', 'Manutech-Ai')

print('Endpoint:', endpoint)
print('Agent:', agent_id)

client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential(), allow_preview=True)
openai_client = client.get_openai_client(agent_name=agent_id)

try:
    resp = openai_client.responses.create(input='Hello from quick_chat.py')
    print('Raw response:', resp)
    # Try to extract text
    if hasattr(resp, 'output') and resp.output:
        out = resp.output[0]
        if hasattr(out, 'content') and out.content:
            print('Assistant text:', getattr(out.content[0], 'text', None))
except Exception as e:
    print('Error during single-run chat:', type(e), e)
    if hasattr(e, 'response') and e.response is not None:
        try:
            print('Response text:', e.response.text)
        except Exception:
            pass
    raise
