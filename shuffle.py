import requests
import sqlalchemy as db
import pandas as pd
import os


def search_artist(artist):
    df.to_sql('songs', con=engine, if_exists='replace')
    query = engine.execute(f"SELECT title FROM songs WHERE artist \
    = '{artist}';").fetchall()
    print(pd.DataFrame(query, columns=['Song Title']))


def delete_artist(artist, df):
    df.drop(df.index[df['artist'] == artist], inplace=True)


def delete_song(song_name, df):
    df.drop(df.index[df['title'] == song_name], inplace=True)


def get_playlist():
    df.to_sql('songs', con=engine, if_exists='replace')
    query_result = engine.execute("SELECT * FROM songs;").fetchall()
    print(pd.DataFrame(query_result, columns=['Number',
                                              'Song Title', 'Artist']))


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
r = requests.get('https://ws.audioscrobbler.com/2.0/',
                 headers=headers, params=payload)
data = r.json()
genresAvailable = []
songs = []

for tag in data['toptags']['tag']:
    genresAvailable.append(tag['name'])
print('These are the genres to choose from: ')
for genre in genresAvailable:
    print(genre + ',', end = ' ')
print("")
print("")

# Input from user picking which genre they would like in the playlist
desiredGenre = input('Please enter a specific genre \
that you want the playlist to have: ')
print('')
parameters = {
    'method': 'tag.gettoptracks',
    'api_key': API_KEY,
    'format': 'json',
    'tag': desiredGenre
}
# Request that gets the top songs that match the chosen genre
topSongs = requests.get(ROOT_URL, headers=headers, params=parameters).json()
playlist = []
artists = []
for song in topSongs['tracks']['track']:
    playlist.append(song['name'])
    artists.append(song['artist']['name'])

# Code to create the database of songs in the playlist
df = pd.DataFrame({'title': playlist, 'artist': artists})
engine = db.create_engine('sqlite:///playlists.db')
df.to_sql('songs', con=engine, if_exists='replace')
get_playlist()

to_query = input('Do you wish to query the playlist Y/N: ')
if to_query.upper() != 'Y':
    to_query = False
else:
    to_query = True
# Code to query the playlist for songs by a certain artist
while to_query is True:
    delete = input('Input "delete" to delete a song or "songs" to see the songs of an artist on the list: ')
    if delete.lower() == 'delete':
        song_or_art = input('Would you like to delete by song name or artist? \nInput \
"song" for song or "artist" for artist: ')
        if song_or_art.lower() == 'song':
            delete_song(input("Enter the name of the song to delete: "), df)
        elif song_or_art.lower() == 'artist':
            delete_artist(input("Enter the name of \
the artist to remove: "), df)
    if delete.lower() == 'songs':
        artist = input('Please enter the name of an artist: ')
        search_artist(artist)
    if input("Continue querying? Y/N: ").upper() != 'Y':
        to_query = False
print("This is the updated playlist: ")
get_playlist()
df.to_csv('playlist.csv', index=False)
