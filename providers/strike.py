import requests
import json
from models import Torrent

def search(query):
	search_url="https://getstrike.net/api/torrents/search/?q=%s" %query
	data=requests.get(search_url).json()
	torrents=[]
	for result in data[1]:
		t=Torrent()
		t.title=result['torrent_title']
		t.seeds=result['seeds']
		t.size=result['size']
		t.torrent_url=result['download_link']
		torrents.append(t)
	return torrents

