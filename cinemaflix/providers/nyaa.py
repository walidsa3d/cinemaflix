import requests

from bs4 import BeautifulSoup as bs
from models import Torrent
from provider import BaseProvider


class Nyaa(BaseProvider):

    def __init__(self, base_url):
        super(Nyaa, self).__init__(base_url)

    def search(self, query):
        search_url = self.base_url
        payload = {'page': 'search', 'term': query,
                   'sort': '2', 'cats': '1_0', 'filter': '0'}
        torrents = []
        response = requests.get(
            search_url, params=payload, headers=self.headers).text
        soup = bs(response, "lxml")
        table = soup.find('table', class_='tlist')
        for tr in table.find_all('tr')[1:]:
            t = Torrent()
            cols = tr.findAll('td')
            t.title = cols[1].find('a').text
            t.size = cols[3].text
            t.seeds = cols[4].text
            t.torrent_url = cols[2].find('a').get('href') + "&magnet=1"
            torrents.append(t)
        return torrents
