import requests
from bs4 import BeautifulSoup as bs
from torrent import Torrent
def search(query):
	base_url='https://rarbg.com'
	headers = {
	'Referer': base_url + '/index6.php',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'
	}
	base_url='http://rarbg.com'
	search_url=base_url+'/torrents.php?category=14;48;17;44;45;47;42;46&search='+query+'&order=seeders&by=DESC'
	print search_url
	response=requests.get(search_url,headers=headers).text
	print response
	soup=bs(response)
	tabl=soup.find('table',attrs={'class':'lista2t'})
	for tr in tabl.find_all('tr'):
		t=Torrent()
		td=tr.find('td')
		t.title=td.findNext('td').find('a').text
		print td.findNext('td')
def get_top():
	pass