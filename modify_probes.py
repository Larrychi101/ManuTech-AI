import json

with open('containerapp-current.json','r') as f:
    cur = json.load(f)

props = cur.get('properties', {})
template = props.get('template', {})
containers = template.get('containers', [])
for c in containers:
    if c.get('name') == 'ca-web-ncbg27q3kcuoi':
        c['probes'] = [
            {"type":"Liveness","failureThreshold":3,"periodSeconds":30,"httpGet":{"path":"/health","port":80}},
            {"type":"Startup","failureThreshold":30,"initialDelaySeconds":5,"periodSeconds":10,"httpGet":{"path":"/health","port":80}}
        ]

body = {'properties': props}
with open('patch-body.json','w') as f:
    json.dump(body,f)
print('WROTE patch-body.json')
