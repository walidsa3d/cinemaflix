import requests
from models import Torrent
from guessit import guess_movie_info
from utils import utils
from provider import BaseProvider

class Kickass(BaseProvider):

    def __init__(self,base_url):
        super(Kickass,self).__init__(base_url)

    def search(self,query):
        payload={'q':query,'field':'seeder','order':'desc','page':'1'}
        search_url = self.base_url + '/json.php'
        data=requests.get(search_url,params=payload,headers=self.headers).json()
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

