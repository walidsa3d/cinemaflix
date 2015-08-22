from __future__ import unicode_literals
from bs4 import BeautifulSoup as bs
from models import Torrent
from guessit import guess_movie_info
from provider import BaseProvider
import re
import requests

class TPB(BaseProvider):

    def __init__(self,base_url):
        super(TPB,self).__init__(base_url)
        

    def search(self,query):
        search_url = self.base_url + "/search/" + query + "/0/7/0"
        data=requests.get(search_url).text
        soup = bs(data,"lxml")
        torrents = []
        for result in soup.find_all('tr')[1:]:
             t = Torrent()
             d = result.find_all('td')
             a = d[1].find_all('a')
             g=guess_movie_info(unicode(a[0].string),info=['filename'])
             t.title=a[0].text
             t.quality=g['screenSize'] if 'screenSize' in g else "Undefined"
             t.torrent_url = a[1]['href']
             t.seeds = int(d[2].text)
             pattern = re.compile("Uploaded (.*), Size (.*), ULed by (.*)")
             match = pattern.match(d[1].font.text)
             t.size = match.groups()[1].replace('xa0',' ')
             torrents.append(t)
        return torrents
    def get_top():
        pass