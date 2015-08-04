import requests
from models import Torrent

def search(query):
    base_url="http://yts.to"
    search_url = base_url + '/api/v2/list_movies.json?query_term=' +query+ '&sort=seeds&order=desc&set=1'
    print search_url
    response=requests.get(search_url).json()
    torrents=[]
    for movie in response['data']['movies']:
        for torrent in movie['torrents']:
            t=Torrent()
            t.title=movie['title_long']+" "+torrent['quality']
            t.seeds=torrent['seeds']
            t.size=torrent['size']
            t.torrent_url=torrent['url']
            torrents.append(t)
    return torrents