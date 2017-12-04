import requests
import json

payload = {'text':'xin chao'}
r = requests.post('http://localhost:5000/', data=json.dumps(payload))
res = json.loads(r.text)
print (res['vector'])