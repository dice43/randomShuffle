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
    'method': 'tag.gettoptags',
    'api_key': API_KEY,
    'format': 'json'
}
# Request to get a list of genres to choose from
r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
data = r.json()
genresAvailable = []
songs = []

for tag in data['toptags']['tag']:
   genresAvailable.append(tag['name'])
print(f'These are the genres to choose from: {genresAvailable}')

# Input from user picking which genre they would like in the playlist
desiredGenre = input('Please enter a specific genre that you want the playlist to have: ')
while desiredGenre not in genresAvailable:
    desiredGenre = input('Please enter a correct genre: ')
print('')
parameters = {
    'method': 'tag.gettoptracks',
    'api_key': API_KEY,
    'format': 'json',
    'tag': desiredGenre
}
# Request that gets the top songs that match the chosen genre
topSongs = requests.get(ROOT_URL, headers=headers, params = parameters).json()
playlist = []
for song in topSongs['tracks']['track']:
    playlist.append(song['name'])
print(f'The playlist is: {playlist}')