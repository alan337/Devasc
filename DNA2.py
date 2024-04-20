import requests
import json
from requests.auth import HTTPBasicAuth

BASE_URL = 'https://sandboxdnac2.cisco.com'
AUTH_ENDPOINT = '/dna/system/api/v1/auth/token'
AUTH_URL = BASE_URL + AUTH_ENDPOINT

response = requests.post(AUTH_URL, auth=HTTPBasicAuth('devnetuser', 'Cisco123!'), verify=False)
TOKEN = response.json()['Token']

FIRST_URL = '/dna/intent/api/v1/network-device'
SECOND_URL = '/dna/intent/api/v1/network-device-poller/cli/read-request'
THIRD_URL = '/dna/intent/api/v1/task/{task_id}'
FOURTH_URL = '/dna/intent/api/v1/file/{file_id}'

headers = {'X-Auth-Token': TOKEN, 'Content-Type': 'application/json'}
params = {'platformId': 'C9KV-UADP-8P'}

# Get network devices
response = requests.get(BASE_URL + FIRST_URL, headers=headers, params=params, verify=False)
devices = [device['id'] for device in response.json()['response']]

# Prepare payload for CLI read request
payload = {
    'commands': ['show version', 'show ip int brief'],
    'deviceUuids': devices,
    'timeout': 0
}

# Perform CLI read request
response = requests.post(BASE_URL + SECOND_URL, data=json.dumps(payload), headers=headers, verify=False)
task_id = response.json()['response']['taskId']

# Check task progress
response = requests.get(BASE_URL + THIRD_URL.format(task_id=task_id), headers=headers, verify=False)
progress_json = json.loads(response.json()['response']['progress'])
file_id = progress_json['fileId']

# Retrieve file content
response = requests.get(BASE_URL + FOURTH_URL.format(file_id=file_id), headers=headers, verify=False)
file_json = response.json()

# Extract and print information from the file
for cmd in file_json:
    print(cmd['commandResponses']['SUCCESS']['show ip int brief'])
