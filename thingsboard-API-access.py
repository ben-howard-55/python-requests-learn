import requests
import json

# Session object allows auth cookies to be managed
s = requests.session()

payload = {'temperature': 60} 

accessToken = HzPOXOov5Dy1LvSPyVGz
# Base URL
url = "https://thingsboard.cloud/api/v1/" + accessToken + "/telemetry"
# post request
r = s.post(url, data=json.dumps(payload))

# should return a 200 status and empty content
print(r)
print(r.content)
