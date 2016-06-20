import requests


import base64
import bencode
import hashlib

import tempfile
from humanize import naturalsize
from bs4 import BeautifulSoup as BS
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
            search_url, headers=self.headers, params=payload, cookies=cookies)
        torrents = self._parse_page(response.text)
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
            try:
                t = Torrent()
                t.title = rows[1].find('a').text
                rarbg_id = rows[1].find('a')['href'].strip('/torrent/')
                title = requests.utils.quote(t.title) + "-[rarbg.com].torrent"
                download_url = self.base_url + "/download.php?id=%s&f=%s" % (
                    rarbg_id, title)
                t.torrent_url = self._to_magnet(download_url)
                t.size = naturalsize(rows[3].text)
                t.seeds = int(rows[4].text)
                torrents.append(t)
            except bencode.BTL.BTFailure:
                pass
        return torrents

    def _to_magnet(self, torrent_link):
        """converts a torrent file to a magnet link"""
        self.headers.update({'Referer': 'https://rarbg.to/torrent/'})
        headers = self.headers
        cookies = {'7fAY799j': 'VtdTzG69'}
        response = requests.get(
            torrent_link, headers=headers, timeout=20, cookies=cookies)
        temp = tempfile.TemporaryFile()
        temp.write(response.content)
        temp.seek(0)
        torrent = temp.read()
        temp.close()
        metadata = bencode.bdecode(torrent)
        hashcontents = bencode.bencode(metadata['info'])
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = base64.b32encode(digest)
        magneturi = 'magnet:?xt=urn:btih:%s' % b32hash
        return magneturi
