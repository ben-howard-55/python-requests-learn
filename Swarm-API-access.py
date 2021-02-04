import requests

# Session object allows auth cookies to be managed
s = requests.session()

# payload to send the body of data in post request
payload = {'username': 'BoatSecure', 'password': '*******'}

# Base URL
url = "https://bumblebee.hive.swarm.space/hive"
# Post request to login to Swarm, were auth cookie is returned
# and stored in the current session
r = s.post(url + "/login", data=payload)
print(s.cookies)
print(r)

# api request to receive all un-seen messages from a specific device
r1 = s.get(url + "/api/v1/messages/2075?deviceid=1610&status=0&direction=fromdevice")
print(r1)
print(r1.content)
