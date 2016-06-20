import requests

from models import Torrent
from provider import BaseProvider
from humanize import naturalsize

class YTS(BaseProvider):

    def __init__(self, base_url):
        super(YTS, self).__init__(base_url)

    def search(self, query):
        payload = {
            'query_term': query, 'sort': 'title', 'order': 'desc', 'set': '1'}
        search_url = self.base_url + '/api/v2/list_movies.json'
        try:
            response = requests.get(
                search_url, params=payload, headers=self.headers).json()
        except Exception:
            return
        torrents = []
        for movie in response['data']['movies']:
            for torrent in movie['torrents']:
                t = Torrent()
                t.title = movie['title_long'] + " " + torrent['quality']
                t.seeds = torrent['seeds']
                t.size = torrent['size']
                t.torrent_url = torrent['url']
                torrents.append(t)
        return torrents

    def get_top(self):
        payload = {
            'sort': 'date_added',
            'order': 'desc',
            'set': '1',
            'limit': 20
        }
        search_url = self.base_url + '/api/v2/list_movies.json'
        try:
            response = requests.get(
                search_url, params=payload, headers=self.headers).json()
        except Exception:
            return
        torrents = []
        for movie in response['data']['movies']:
            for torrent in movie['torrents']:
                t = Torrent()
                t.title = movie['title_long'] + " " + torrent['quality']
                t.seeds = torrent['seeds']
                t.size = torrent['size']
                t.torrent_url = torrent['url']
                torrents.append(t)
        return torrents
