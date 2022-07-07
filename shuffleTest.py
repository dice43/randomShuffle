import unittest
import os
import pandas as pd
import sqlalchemy as df
import requests
from shuffle import search_artist


class ShuffleTest(unittest.TestCase):

    def setUp(self):
        self.API_KEY = os.environ.get('API_KEY')
        self.USER_AGENT = "user"
        # Root url of the api
        self.ROOT_URL = 'http://ws.audioscrobbler.com/2.0/'

        self.headers = {
            'user-agent': self.USER_AGENT
        }
        # Parameters that need to be passed to the get request
        self.payload = {
            'method': 'tag.gettoptags',
            'api_key': self.API_KEY,
            'format': 'json'
        }
        # Request to get a list of genres to choose from
        self.r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=self.headers, params=self.payload)

    def test_request_genre_status(self):
        self.assertEqual(200,self.r.status_code)

    def test_request_songs(self):
        self.payload['method'] = 'tag.gettoptracks'
        topSongs = requests.get(self.ROOT_URL, headers = self.headers, params = self.payload)
        self.assertEqual(200,topSongs.status_code)

if __name__ == '__main__':
    unittest.main()