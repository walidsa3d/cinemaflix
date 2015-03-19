import requests
from torrent import Torrent
from pyquery import PyQuery
def search(query):
    search_url = "https://oldpiratebay.org/search.php?q=%s&iht=5&sort=-seeders" %query
    torrents = []
    pq = PyQuery(url=search_url)
    for tr in pq('table.result').find('tr').items():
        t=Torrent()
        t.title=tr.find('td').eq(1).find('a').text()
        t.torrent_url=tr.find('td').eq(1).find('a').eq(2).attr('href')
        t.size=tr.find('td').eq(3).text()
        t.seeds=tr.find('td').eq(4).text()
        torrents.append(t)
    return torrents

