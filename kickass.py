import requests
import math
from torrent import Torrent
from guessit import guess_movie_info
def search(query):
        url="http://kickass.to"
        search_url = url + '/json.php?q=' + query + '&field=seeders&order=desc&page=1'
        print search_url
        data=requests.get(search_url).json()
        torrents=[]
        for movie in data['list']:
            t=Torrent()
            g=guess_movie_info(movie['title'],info=['filename'])
            t.title=g['title']
            t.quality=g['screenSize'] if 'screenSize' in g else "Undefined"
            t.seeds=str(movie['seeds'])
            t.size=ToSize(movie['size'])
            t.torrent_url=movie['torrentLink']
            torrents.append(t)
        return torrents

  
def ToSize(bytes):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if bytes == 0:
        return "0 Byte"
    i = int(math.floor(math.log(bytes) / math.log(1024)))
    r=round(bytes / math.pow(1024, i), 2) 
    return str(r)+ '' + sizes[i]