import requests
from bs4 import BeautifulSoup as bs
from torrent import Torrent

def search(query):
    url = "https://oldpiratebay.org/search.php?q=%s" %query
    response = requests.get(url)
    soup = bs(response.text)
    print soup.select("#w0 > div.panel.panel-default > div.table-responsive > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > a")
    torrents = []
    for torrent in soup.findAll('tr'):
        t=Torrent()
        t.size = torrent.find('td', attrs={'class': 'size-row'})
        t.seeds = torrent.find('td', attrs={'class': 'seeders-row'})
        t.torrent_url = torrent.find('a', attrs={'title': 'MAGNET LINK'})['href']
        t.title=torrent.find('span').text
        torrents.append(t)
    return torrents

search("gladiator")