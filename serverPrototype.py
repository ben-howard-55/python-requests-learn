import asyncio
import requests
import json
import base64
import time

# Author: Benjamin Howard
# date: 04-02-2021

# --- swarm API information ----------------------------------

# payload to send the body of data in post request
swarmAuth = {'username': 'BoatSecure', 'password': '?A:7S]9zj7{Z-:pv'}
swarmURL = "https://bumblebee.hive.swarm.space/hive" # Base URL
userApplicationId = 2075 # boatsecure user application ID

# params for getting 1 message from the swarmAPI
swarmParams={'deviceid': '1610', 'status': 0, 'direction': 'fromdevice', 'count': 1}
# path for getting message information for a specific userId
swarmMessagePath="/api/v1/messages/" + str(userApplicationId)
swarmReceived = "/rxack/"

# --- ThingsBoard Cloud API information -----------------------


# base thingsboard cloudn url
thingsBoardURL = "https://thingsboard.cloud/api/v1/"
thingsBoardDeviceId = "TileId-1610"

# things board telemetry path
thingsBoardPath = thingsBoardDeviceId + "/telemetry"

# --- Function Definitions ------------------------------------

# formats the returned swarm data, returns packetId and data
def formatSwarmData(content):
    for message in content:
        data = message["data"]
        packetId = message["packetId"]

        # decode the base64 response to a string
        base64_bytes = data.encode('ascii')
        data_bytes = base64.b64decode(base64_bytes)
        data = data_bytes.decode('ascii')

        # split the data object (temporary)
        dataComponents = data.split(',')
        # create the data structure to send
        dataObject = {'latitude': dataComponents[1], 'longitude': dataComponents[2]}

        print(data, dataObject, packetId)
        return (dataObject, packetId)


# api post request to update thingsBoard Cloud to specific device
async def postToThingsBoard(url, path, dataObject):
    response = requests.post(url + path, data=json.dumps(dataObject))
    print(response)

# api request to receive 1st unseen message in Swarm queue from a specific device
async def getSwarmMessage(url, path, params):
    response = s.get(url + path, params=params)
    print(response.json())
    return response.json()

async def acknowledgeSwarmPacketReceived(packetId):
    response = s.get(swarmURL + swarmMessagePath + swarmReceived + str(packetId))
    print(response, response.content)


async def main():
    while True:
        # get a single message from swam API
        msgResponse = await getSwarmMessage(swarmURL, swarmMessagePath, swarmParams)
        # get the data and packetId from swarmAPI
        dataObject, packetId = formatSwarmData(msgResponse)
        # TODO: mark data as collected
        await acknowledgeSwarmPacketReceived(packetId)
        # send data to thingsBoard Cloud
        await postToThingsBoard(thingsBoardURL, thingsBoardPath, dataObject)
        time.sleep(5)

# --- LOGIN to SWARM API / START --------------------------------------

# Session object allows auth cookies to be managed
s = requests.session()

# Post request to login to Swarm, were auth cookie is returned and stored in the current session
r = s.post(swarmURL + "/login", data=swarmAuth)
print(s.cookies)
print(r)

# run main loop
asyncio.run(main())
