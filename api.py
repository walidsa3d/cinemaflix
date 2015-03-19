import providers.yts as yts
import providers.kickass as kickass
import providers.tpb as tpb
import providers.nyaa as nyaa
import providers.limetorrents as lime
from providers.t411 import T411 as t411
import providers.cpabsien as cpabsien
import providers.oldpiratebay as oldtpb
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
    return results
def sort_results(torrent_list,criteria):
    return sorted(torrent_list,key=attrgetter(criteria),reverse=True)
def filter_results(torrent_list,criteria):
    return [x for x in torrent_list if x['seeds']>=100]