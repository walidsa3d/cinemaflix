import requests


from humanize import naturalsize
from bs4 import BeautifulSoup as BS
from models import Torrent
from provider import BaseProvider


class Kickass(BaseProvider):

    def __init__(self, base_url):
        super(Kickass, self).__init__(base_url)

    def search(self, query):
        payload = {'q': query, 'field': 'seeder', 'order': 'desc', 'page': '1'}
        search_url = self.base_url + '/json.php'
        data = requests.get(
            search_url, params=payload, headers=self.headers).json()
        torrents = []
        for movie in data['list']:
            t = Torrent()
            t.title = movie['title']
            t.seeds = int(movie['seeds'])
            t.size = naturalsize(movie['size'])
            t.torrent_url = movie['torrentLink']
            torrents.append(t)
        return torrents

    def get_top(self):
        search_url = self.base_url + '/movies'
        data = requests.get(search_url, headers=self.headers).text
        soup = BS(data, "lxml")
        torrents = []
        table = soup.find(class_="data")
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            t = Torrent()
            t.title = cells[0].find(class_="cellMainLink").text
            t.torrent_url = cells[0].find_all("a")[3].get('href')
            t.size = cells[1].text
            t.seeds = int(cells[4].text)
            torrents.append(t)
        return torrents
