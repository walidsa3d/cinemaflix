import requests
from bs4 import BeautifulSoup as bs
from torrent import Torrent

def search(query):
    search_url = "https://oldpiratebay.org/search.php?q=%s" %query
    response = requests.get(search_url)
    soup = bs(response.text)
    torrents = []
    for tr in soup.findAll('tr'):
        t=Torrent()
        cols = tr.find_all('td')[1:]
        print cols[1].find('a')
        torrents.append(t)
    return torrents

search("gladiator")