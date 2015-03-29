import requests
import math
from models import Torrent
from guessit import guess_movie_info
from utils.torrentutils import torrentutils

def search(query):
        base_url="http://kickass.to"
        search_url = base_url + '/json.php?q=' + query + '&field=seeders&order=desc&page=1'
        data=requests.get(search_url).json()
        torrents=[]
        for movie in data['list']:
            t=Torrent()
            g=guess_movie_info(movie['title'],info=['filename'])
            t.title=movie['title']
            t.seeds=int(movie['seeds'])
            t.size=torrentutils().hsize(movie['size'])
            t.torrent_url=movie['torrentLink']
            torrents.append(t)
        return torrents

