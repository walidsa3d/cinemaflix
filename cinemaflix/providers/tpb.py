from __future__ import unicode_literals

import re

import requests

from bs4 import BeautifulSoup as BS
from models import Torrent
from provider import BaseProvider


class TPB(BaseProvider):

    def __init__(self, base_url):
        super(TPB, self).__init__(base_url)

    def search(self, query):
        search_url = self.base_url + "/search/" + query + "/0/7/0"
        response = requests.get(search_url).text
        torrents = self._parse_page(response)
        return torrents

    def get_top(self):
        search_url = self.base_url + "/browse/201/0/7/0"
        response = requests.get(search_url).text
        torrents = self._parse_page(response)
        return torrents

    def _parse_page(self, page_text):
        soup = BS(page_text, "lxml")
        torrents = []
        table = soup.find(id="searchResult")
        for row in table.find_all('tr')[1:30]:
            t = Torrent()
            cells = row.find_all('td')
            a = cells[1].find_all('a')
            t.title = a[0].text
            t.torrent_url = a[1]['href']
            t.seeds = int(cells[2].text)
            pattern = re.compile("Uploaded (.*), Size (.*), ULed by (.*)")
            match = pattern.match(cells[1].font.text)
            t.size = match.groups()[1].replace('xa0', ' ')
            torrents.append(t)
        return torrents
