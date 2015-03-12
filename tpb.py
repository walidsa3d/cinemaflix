import requests
from bs4 import BeautifulSoup as bs
from torrent import Torrent
from guessit import guess_movie_info
import re
def search(query):
    url="https://thepiratebay.se"
    search_url = url + "/search/" + query + "/0/7/0"
    data=requests.get(search_url).text
    soup = bs(data)
    torrents = []
    for result in soup.find_all('tr')[1:]:
         t = Torrent()
         d = result.find_all('td')
         a = d[1].find_all('a')
         g=guess_movie_info(unicode(a[0].string),info=['filename'])
         year=str(g['year']) if 'year' in g else ""
         t.title=g['title']+" "+year
         t.quality=g['screenSize'] if 'screenSize' in g else "Undefined"
         t.torrent_url = a[1]['href']
         t.seeds = int(d[2].text)
         pattern = re.compile("Uploaded (.*), Size (.*), ULed by (.*)")
         match = pattern.match(d[1].font.text)
         # t.size = match.groups()[1].replace('xa0',' ')
         torrents.append(t)
    return torrents
    