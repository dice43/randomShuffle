import requests
import sqlalchemy as db
import pandas as pd
import os

def search_artist(artist):
    
    query = engine.execute(f"SELECT title FROM songs WHERE artist = '{artist}';").fetchall()
    print(pd.DataFrame(query, columns=['Song Title']))

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
artists = []
for song in topSongs['tracks']['track']:
    playlist.append(song['name'])
    artists.append(song['artist']['name'])
print(f'The playlist is: {playlist}')

# Code to create the database of songs in the playlist
df = pd.DataFrame({'title': playlist, 'artist': artists})
engine = db.create_engine('sqlite:///playlists.db')
df.to_sql('songs', con=engine, if_exists='replace')
query_result = engine.execute("SELECT * FROM songs;").fetchall()
print(pd.DataFrame(query_result, columns=['Number','Song Title','Artist']))

# Code to query the playlist for songs by a certain artist
to_query = input('Do you wish to query the playlist Y/N: ')
if to_query.upper() != 'Y':
    quit()
artist = input('Please input an artist\'s name to search for: ')
search_artist(artist)
