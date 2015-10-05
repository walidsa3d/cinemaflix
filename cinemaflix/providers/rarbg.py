import requests

from bs4 import BeautifulSoup as BS
from cinemaflix.utils.utils import utils
from models import Torrent
from provider import BaseProvider


class Rarbg(BaseProvider):

    def __init__(self, base_url):
        super(Rarbg, self).__init__(base_url)

    def search(self, query):
        payload = {'category': '14;48;17;44;45;47;42;46',
                   'search': query, 'order': 'seeder', 'by': 'DESC'}
        search_url = self.base_url + '/torrents.php'
        cookies = {'7fAY799j': 'VtdTzG69'}
        response = requests.get(
            search_url, headers=self.headers, params=payload, cookies=cookies).text
        torrents = self._parse_page(response)
        return torrents

    def get_top(self):
        top_url = "https://rarbg.to/torrents.php?category=14;48;17;44;45;47;42;46&search=rarbg&order=seeders&by=DESC&page=1"
        cookies = {'7fAY799j': 'VtdTzG69'}
        response = requests.get(
            top_url, headers=self.headers, cookies=cookies).text
        torrents = self._parse_page(response)
        return torrents

    def _parse_page(self, page_text):
        soup = BS(page_text, "lxml")
        tabl = soup.find('table', class_='lista2t')
        torrents = []
        for tr in tabl.find_all('tr')[1:]:
            rows = tr.find_all('td')
            t = Torrent()
            t.title = rows[1].find('a').text
            rarbg_id = rows[1].find('a')['href'].strip('/torrent/')
            title = requests.utils.quote(t.title) + "-[rarbg.com].torrent"
            t.torrent_url = self.base_url + "/download.php?id=%s&f=%s" % (
                rarbg_id, title)
            t.size = rows[4].text
            t.seeds = rows[5].text
            torrents.append(t)
        return torrents
