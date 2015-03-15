import requests
from bs4 import BeautifulSoup as bs
from torrent import Torrent
from guessit import guess_movie_info

def search(query):
    base_url="http://www.nyaa.se/"
    search_url = base_url + "/?page=search&term=" + query + "&sort=2&cats=1_0&filter=0"
    torrents=[]
    response=requests.get(search_url).text
    soup=bs(response)
    table = soup.find('table', attrs={'class':'tlist'})
    for tr in table.find_all('tr')[1:]:
        t=Torrent()
        cols = tr.findAll('td')
        g=guess_movie_info(cols[1].find('a').text,info=['filename'])
        t.title=cols[1].find('a').text
        t.size=cols[3].text
        t.seeds=cols[4].text
        t.torrent_url=cols[2].find('a').get('href')+"&magnet=1"
        t.quality=g['screenSize'] if 'screenSize' in g else "Undefined"
        torrents.append(t)
    return torrents

