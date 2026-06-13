import json
import subprocess
import sys
uri = "https://management.azure.com/subscriptions/cd2b8ef3-5c1e-47f0-8859-41c3bcffef17/resourceGroups/rg-manutech-ai/providers/Microsoft.App/containerApps/ca-web-ncbg27q3kcuoi?api-version=2026-03-02-preview"
print('GET', uri)
proc = subprocess.run(["az","rest","--method","GET","--uri",uri,"-o","json"], capture_output=True, text=True)
if proc.returncode != 0:
    print('az rest GET failed', proc.returncode, proc.stderr)
    sys.exit(1)
obj = json.loads(proc.stdout)
containers = obj.get('properties',{}).get('template',{}).get('containers',[])
changed = False
for c in containers:
    probes = c.get('probes')
    if probes:
        for p in probes:
            http = p.get('httpGet')
            if http and http.get('port') == 8080:
                http['port'] = 80
                changed = True
if not changed:
    print('No probe ports equal to 8080 found; nothing to change')
body = {'properties': {'template': obj.get('properties',{}).get('template',{})}}
with open('patch-probes.json','w', encoding='utf8') as f:
    json.dump(body, f, indent=2)
print('Wrote patch-probes.json')
proc2 = subprocess.run(["az","rest","--method","PATCH","--uri",uri,"--headers","{\"Content-Type\":\"application/json\"}","--body","@patch-probes.json","-o","json"], capture_output=True, text=True)
print('PATCH exit', proc2.returncode)
if proc2.stdout:
    print(proc2.stdout)
if proc2.stderr:
    print(proc2.stderr)
sys.exit(proc2.returncode)
