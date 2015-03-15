import requests
from bs4 import BeautifulSoup as bs
from torrent import Torrent

def search(query):
    search_url = "https://oldpiratebay.org/search.php?q=%s" %query
    response = requests.get(search_url)
    soup = bs(response.text)
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