import requests
import json
import math

def yts_search(query):
    url="http://yts.re"
    search_url = url + '/api/v2/list_movies.json?query_term=' +query+ '&sort=seeds&order=desc&set=1'
    response=requests.get(search_url)
    data=json.loads(response.text)
    for movie in data['data']['movies']:
        print movie['title_long']
     
def kickass_search(query):
    url="http://kickass.to"
    search_url = url + '/json.php?q=' + query + '&field=seeders&order=desc&page=1'
    response=requests.get(search_url)
    data=json.loads(response.text)
    for movie in data['list']:
        print movie['title']+" "+str(movie['seeds'])+" "+ToSize(movie['size'])

def tpb_search(query):
    url="http://thepiratebay.se"
    search_url = url + "/search/" + query + "/0/7/0"
    print search_url


    
def ToSize(bytes):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if bytes == 0:
        return "0 Byte"
    i = int(math.floor(math.log(bytes) / math.log(1024)))
    r=round(bytes / math.pow(1024, i), 2) 
    return str(r)+ '' + sizes[i]

kickass_search("gladiator")