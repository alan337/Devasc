import requests
from requests.auth import HTTPBasicAuth

BASE_URL = 'https://sandboxdnac2.cisco.com'
AUTH_ENDPOINT = '/dna/system/api/v1/auth/token'

# Construct the full authentication URL
AUTH_URL = BASE_URL + AUTH_ENDPOINT
response = requests.post(AUTH_URL, auth=HTTPBasicAuth('devnetuser', 'Cisco123!'), verify=False)
TOKEN = response.json()['Token']

headers = {'X-Auth-Token': TOKEN, 'Content-Type': 'application/json'}

DEVICES_COUNT_URI = '/dna/intent/api/v1/network-device/count'
DEVICES_URL = '/dna/intent/api/v1/network-device'
DEVICES_BY_ID_URL = '/dna/intent/api/v1/network-device/'

def devices_func(headers):
    response = requests.get(BASE_URL + DEVICES_COUNT_URI, headers=headers, verify=False)
    return response.json()

def devices_test(headers, query_string_params):
    response = requests.get(BASE_URL + DEVICES_URL, headers=headers, params=query_string_params, verify=False)
    return response.json()

def device_info(headers, device_id):
    response = requests.get(BASE_URL + DEVICES_BY_ID_URL + device_id, headers=headers, verify=False)
    return response.json()

print(devices_func(headers))
print(devices_test(headers, {}))
print(devices_test(headers, {'hostname': 'sw1.ciscotest.com'}))
response = devices_test(headers, {'platformId': 'C9KV-UADP-8P'})
print(response['response'][0]['hostname'])
print(device_info(headers, response['response'][0]['id']))
