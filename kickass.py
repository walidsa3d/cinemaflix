import requests
import math
from torrent import Torrent
def search(query):
        url="http://kickass.to"
        search_url = url + '/json.php?q=' + query + '&field=seeders&order=desc&page=1'
        data=requests.get(search_url).json()
        torrents=[]
        for movie in data['list']:
            t=Torrent()
            t.title=movie['title']
            t.seeds=str(movie['seeds'])
            t.size=ToSize(movie['size'])
            torrents.append(t)
        return torrents

  
def ToSize(bytes):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if bytes == 0:
        return "0 Byte"
    i = int(math.floor(math.log(bytes) / math.log(1024)))
    r=round(bytes / math.pow(1024, i), 2) 
    return str(r)+ '' + sizes[i]