import requests

# Make an HTTP GET request
response = requests.get('https://www.cisco.com', timeout=5)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the content of the response
    print(response.iter_content)

