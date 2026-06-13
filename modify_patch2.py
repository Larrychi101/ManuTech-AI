import json

with open('patch-body.json','r') as f:
    body = json.load(f)

containers = body['properties']['template']['containers']
for c in containers:
    if c.get('name') == 'ca-web-ncbg27q3kcuoi':
        # update env
        env = c.get('env', [])
        for e in env:
            if e.get('name') == 'ASPNETCORE_URLS':
                e['value'] = 'http://+:80'
        # update probes
        c['probes'] = [
            {"type":"Liveness","failureThreshold":3,"periodSeconds":30,"httpGet":{"path":"/health","port":80}},
            {"type":"Startup","failureThreshold":30,"initialDelaySeconds":5,"periodSeconds":10,"httpGet":{"path":"/health","port":80}}
        ]

with open('patch-body2.json','w') as f:
    json.dump(body,f)
print('WROTE patch-body2.json')
