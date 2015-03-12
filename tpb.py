import requests
import BeautifulSoup as bs

def search(query):
    url="http://thepiratebay.se"
    search_url = url + "/search/" + query + "/0/7/0"
    print search_url