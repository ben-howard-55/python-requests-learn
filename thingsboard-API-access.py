import requests
import json

# Session object allows auth cookies to be managed
s = requests.session()

# payload to send the body of data in post request
# payload = {'username': 'bjhoward5555@gmail.com', 'password': '4P2pABJ36JH4cJ@'}
payload = {'temperature': 60} 
# headers = {'Content-Type': 'application/json'}


# Base URL
url = "https://thingsboard.cloud/api/v1/HzPOXOov5Dy1LvSPyVGz/telemetry"
r = s.post(url, data=json.dumps(payload))

print(r)
print(r.content)