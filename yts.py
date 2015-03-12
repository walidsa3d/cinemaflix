import requests
from torrent import Torrent

def search(query):
    url="http://yts.re"
    search_url = url + '/api/v2/list_movies.json?query_term=' +query+ '&sort=seeds&order=desc&set=1'
    data=requests.get(search_url).json()
    torrents=[]
    for movie in data['data']['movies']:
        for torrent in movie['torrents']:
	        t=Torrent()
	        t.title=movie['title_long']+" "+torrent['quality']
	        t.seeds=torrent['seeds']
	        t.size=torrent['size']
	        t.torrent_url=torrent['url']
	        torrents.append(t)
    return torrents