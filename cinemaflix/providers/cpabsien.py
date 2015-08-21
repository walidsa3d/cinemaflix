import requests
from bs4 import BeautifulSoup as bs
from models import Torrent
from provider import BaseProvider

class cpabsien(BaseProvider):

	def __init__(self):
		self.base_url="http://www.cpasbien.pw/recherche/films/"

	def search(self,query):
		search_url=self.base_url+query+".html,trie-seeds-d"
		response=requests.get(search_url).text
		soup=bs(response,"lxml")
		torrents=[]
		lines=soup.find_all('div',attrs={'class':'ligne0'})+soup.find_all('div',attrs={'class':'ligne1'})
		for line in lines :
			t=Torrent()
			t.title=line.find('a').text
			t.size=line.find('div',attrs={'class':'poid'}).text
			t.seeds=int(line.find('span',attrs={'class':'seed_ok'}).text)
			t.torrent_url=self._torrent_link(line.find('a').get('href'))
			torrents.append(t)
		return torrents

	def _torrent_link(self,page_url):
		response=requests.get(page_url).text
		soup=bs(response,"lxml")
		relative_link=soup.find('a',attrs={'id':'telecharger'}).get('href')
		return "http://www.cpasbien.pw"+relative_link

