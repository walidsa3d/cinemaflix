import requests
from bs4 import BeautifulSoup as bs

def search(query):
    url='http://extratorrent.cc/search/?search=%s' %query
    response=requests.get(url).text
    soup=bs(response)
    torrents = []
    for :
        
        torrents.append(item)
    return results


print search("gladiator")