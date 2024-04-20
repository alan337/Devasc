import requests, json

device = {
    "ip": "192.168.100.80",
    "username": "admin",
    "password": "admin",
    "port": "443",
}

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

module = "ietf-interfaces:interfaces-state"
url = f"https://{device['ip']}:{device['port']}/restconf/data/{module}"

requests.packages.urllib3.disable_warnings()
response = requests.get(url, headers=headers, auth=(device['username'], device['password']), verify=False).json()

interfaces = response['ietf-interfaces:interfaces-state']['interface']
for interface in interfaces:
    if bool(interface['admin-status']):
#       print(f"{interface['name']} -- {interface['description']} {interface['ietf-ip:ipv4']['address'][0]['ip']}")
        print(f"{interface['name']} ")
