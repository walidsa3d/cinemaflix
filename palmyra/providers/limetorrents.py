import requests
from bs4 import BeautifulSoup as bs
from models import Torrent

def search(query):
    base_url="http://www.limetorrents.in/"
    search_url=base_url+"search/movies/"+query+"/seeds/1/"
    response=requests.get(search_url).text
    soup=bs(response)
    torrents=[]
    table=soup.find_all('table',attrs={'class':'table2'})[1]
    for tr in table.find_all('tr')[1:]:
        t=Torrent()
        t.title=tr.select('.tt-name a')[1].text
        t.size=tr.select('.tdnormal')[1].text
        t.seeds=int(tr.select('.tdseed')[0].text)
        t.torrent_url=tr.select('.tt-name a')[0].get('href')
        torrents.append(t)
    return torrents
