import yts as yts
import kickass as kickass
import tpb as tpb
import nyaa as nyaa
import limetorrents as lime
from t411 import T411 as t411
import cpabsien as cpabsien
import oldpiratebay as oldtpb
import strike as strike
from operator import attrgetter

def search(query,provider):
    results=[]
    if(provider=="kickass"):
         results=kickass.search(query)
    if(provider=="yts"):
         results=yts.search(query)
    if(provider=="thepiratebay"):
         results=tpb.search(query)
    if(provider=="oldpiratebay"):
         results=oldtpb.search(query)
    if(provider=="limetorrents"):
         results=lime.search(query)
    if(provider=="cpabsien"):
         results=cpabsien.search(query)
    if(provider=="t411"):
         results=t411().search(query)
    if(provider=="strike"):
         results=strike.search(query)
    if(provider=="nyaa"):
         results=nyaa.search(query)
    return results[:50]
    
def sort_results(torrent_list,criteria):
    return sorted(torrent_list,key=attrgetter(criteria),reverse=True)
def filter_results(torrent_list,criteria):
    return [x for x in torrent_list if x['seeds']>=100]