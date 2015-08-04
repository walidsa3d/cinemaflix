import requests
from models import Torrent
import re
import json

class eztv:
	def __init__(self):
		self.shows=[]
		self.base_url="http://eztvapi.re/"
	def get_shows(self):
		shows_url=self.base_url+"shows/"
		data=requests.get(shows_url).json()
		shows=[]
		for url in [shows_url+unicode(x) for x in xrange(1,16)]:
			data=requests.get(url).json()
			for show in data:
				shows.append({'id':show['imdb_id'], 'title':show['title']})
		return shows
	def get_shows_from_cache(self):
		with open("cache.json",'w') as f:
			shows=json.load(f)
		return shows

	def search_show(self,query):
		with open("providers/cache.json","r") as f:
			shows=json.load(f)
		results=[]
		for show in shows:
			match=re.search(query.lower(),show['title'].lower())
			if match:
				results.append(show)
		return results

	def cache_shows(self):
		shows=self.get_shows()
		with open("cache.json",'w') as f:
			f.write(json.dumps(shows))

	def get_episodes(self,show_id):
		show_url=self.base_url+"show/"+show_id
		print show_url
		data=requests.get(show_url).json()
		episodes=[]
		for episode in data['episodes']:
			episodes.append({'num':episode['episode'],'season':episode['season'],'title':episode['title'], 'torrent_url':episode['torrents']["0"]['url'],'seeds':episode['torrents']["0"]['seeds']})
		episodes=sorted(episodes,key=lambda k: (k['season'],k['num']))
		return episodes
	def search_episode(self,showname,s,e,episodes):
		t=Torrent()
		torrents=[]
		for episode in episodes:
			if s==episode['season'] and episode['num']==e:
				t.title=showname+'.'+'S'+str(s)+'E'+str(e)+':'+episode['title']
				t.torrent_url=episode['torrent_url']
				t.seeds=episode['seeds']
				torrents.append(t)
		return torrents

	def display_episodes(self,episodes):
		for episode in episodes:
			print 'S%sE%s||%s' %(episode['season'],episode['num'], episode['title'])
	def search(self,showname,season,episode):
		show=self.search_show(showname)[0]
		season=int(season)
		episode=int(episode)
		all_episodes=self.get_episodes(show['id'])
		torrents=self.search_episode(show['title'],season,episode,all_episodes)
		return torrents

if __name__ == '__main__':
	eztv=eztv()

