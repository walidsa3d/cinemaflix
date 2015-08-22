import requests
from bs4 import BeautifulSoup as bs
from models import Torrent
from provider import BaseProvider

class Rarbg(BaseProvider):


	def __init__(self,base_url):
		super(Rarbg,self).__init__(base_url)

	def search(self,query):
		payload={'category':'14;48;17;44;45;47;42;46','search':query,'order':'seeder','by':'DESC'}
		search_url=self.base_url+'/torrents.php'
		response=requests.get(search_url,headers=headers,params=payload).text
		soup=bs(response,"lxml")
		tabl=soup.find('table',attrs={'class':'lista2t'})
		for tr in tabl.find_all('tr'):
			t=Torrent()
			t.title=tr.find_all('td')[1].find('a').text
			print t.title
	def get_top():
		pass

if __name__ == '__main__':
	Rarbg("https://rarbg.com").search("jurassic")