import requests
from models import Torrent
from guessit import guess_movie_info
from utils import utils
from provider import BaseProvider

class kickass(BaseProvider):

    def __init__(self):
        self.base_url="http://kickass.to"

    def search(self,query):
            search_url = self.base_url + '/json.php?q=' + query + '&field=seeders&order=desc&page=1'
            data=requests.get(search_url).json()
            torrents=[]
            for movie in data['list']:
                t=Torrent()
                g=guess_movie_info(movie['title'],info=['filename'])
                t.title=movie['title']
                t.seeds=int(movie['seeds'])
                t.size=utils.hsize(movie['size'])
                t.torrent_url=movie['torrentLink']
                torrents.append(t)
            return torrents

