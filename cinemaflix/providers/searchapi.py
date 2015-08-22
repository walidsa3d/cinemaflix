# walid.saad

from yts import YTS
from kickass import Kickass
from tpb import TPB
from nyaa import Nyaa
from t411 import T411
from cpabsien import Cpabsien
from strike import Strike
from eztv import Eztv
from redditmovies import redditmovies
from redditdocus import redditdocus
from operator import attrgetter
from constants import *

def search(query, provider, sort=None, seeds=0, max=0):
    results = []
    sorts = ['seeds', 'size']
    if(provider == "kickass"):
        results = Kickass(KICKASS_URL).search(query)
    elif(provider == "redditmovies"):
        results = redditmovies().search(query)
    elif(provider == "redditdocus"):
        results = redditdocus().search(query)
    elif(provider == "yts"):
        results = YTS(YTS_URL).search(query)
    elif(provider == "thepiratebay"):
        results = TPB(TPB_URL).search(query)
    elif(provider == "cpabsien"):
        results = Cpabsien(CPABSIEN_URL).search(query)
    elif(provider == "t411"):
        results = T411().search(query)
    elif(provider == "strike"):
        results = Strike().search(query)
    elif(provider == "nyaa"):
        results = Nyaa(NYAA_URL).search(query)
    elif(provider == "eztv"):
        results = Eztv(EZTV_URL).search(query)
    sorted_results=sort_results(results,sort) if sort in sorts else results
    filtered_results = filter(lambda x:x.seeds>=seeds, sorted_results)
    final_results = filtered_results[:max]
    return final_results


def sort_results(torrent_list, criteria):
    return sorted(torrent_list, key=attrgetter(criteria), reverse=True)
