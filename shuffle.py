import requests
import os

# Constants to get api key from environment variables
API_KEY = os.environ.get('API_KEY')
USER_AGENT = "user"
# Root url of the api
ROOT_URL = 'http://ws.audioscrobbler.com/2.0/'

headers = {
    'user-agent': USER_AGENT
}
# Parameters that need to be passed to the get request
payload = {
    'method': 'chart.gettoptags',
    'api_key': API_KEY,
    'format': 'json'
}

r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
print(r.status_code)
print(r.json())
