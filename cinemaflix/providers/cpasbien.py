import requests

from bs4 import BeautifulSoup as BS
from models import Torrent
from provider import BaseProvider


class Cpasbien(BaseProvider):

    def __init__(self, base_url):
        super(Cpasbien, self).__init__(base_url)

    def search(self, query):
        search_url = "{}{}{}".format(
            self.base_url,
            query,
            ".html,trie-seeds-d"
        )
        response = requests.get(search_url).text
        torrents = self._parse_page(response)
        return torrents

    def _torrent_link(self, page_url):
        response = requests.get(page_url).text
        soup = BS(response, "lxml")
        relative_link = soup.find('a', id='telecharger').get('href')
        return "http://www.cpasbien.io" + relative_link

    def get_top(self):
        top_url = "http://www.cpasbien.io/view_cat.php?categorie=films&trie=seeds-d"
        response = requests.get(top_url).text
        torrents = self._parse_page(response)
        return torrents

    def _parse_page(self, page_text):
        soup = BS(page_text, "lxml")
        torrents = []
        lines = soup.find_all(class_='ligne0') + soup.find_all(class_='ligne1')
        for line in lines:
            t = Torrent()
            t.title = line.find('a').text
            t.size = line.find(class_='poid').text
            t.seeds = int(line.find(class_='seed_ok').text)
            t.torrent_url = self._torrent_link(line.find('a').get('href'))
            torrents.append(t)
        return torrents
