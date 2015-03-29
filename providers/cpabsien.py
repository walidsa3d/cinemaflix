import requests
from bs4 import BeautifulSoup as bs
from models import Torrent

def search(query):
	base_url="http://www.cpasbien.pw/recherche/films/"
	search_url=base_url+query+".html,trie-seeds-d"
	response=requests.get(search_url).text
	soup=bs(response)
	torrents=[]
	lignes=soup.find_all('div',attrs={'class':'ligne0'})+soup.find_all('div',attrs={'class':'ligne1'})
	for ligne in lignes :
		t=Torrent()
		t.title=ligne.find('a').text
		t.size=ligne.find('div',attrs={'class':'poid'}).text
		t.seeds=int(ligne.find('span',attrs={'class':'seed_ok'}).text)
		t.torrent_url=get_torrent_link(ligne.find('a').get('href'))
		torrents.append(t)
	return torrents

def get_torrent_link(page_url):
	response=requests.get(page_url).text
	soup=bs(response)
	relative_link=soup.find('a',attrs={'id':'telecharger'}).get('href')
	return "http://www.cpasbien.pw"+relative_link

