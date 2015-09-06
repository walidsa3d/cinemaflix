# walid.saad

from yts import YTS
from kickass import Kickass
from tpb import TPB
from nyaa import Nyaa
from t411 import T411
from cpabsien import Cpabsien
from strike import Strike
from eztv import Eztv
from rarbg import Rarbg
from operator import attrgetter
from constants import *

def search(query, provider, sort=None, seeds=0, max=0):
    sorts = ['seeds', 'size']
    results={
    "kickass": Kickass(KICKASS_URL),
    "rarbg": Rarbg(RARBG_URL),
    "yts": YTS(YTS_URL),
    "thepiratebay": TPB(TPB_URL),
    "cpabsien": Cpabsien(CPABSIEN_URL),
    "strike": Strike(STRIKE_URL),
    "nyaa":Nyaa(NYAA_URL),
    "eztv":Eztv(EZTV_URL)
    }.get(provider,'tpb').search(query)
    sorted_results=sort_results(results,sort) if sort in sorts else results
    filtered_results = filter(lambda x:x.seeds>=seeds, sorted_results)
    final_results = filtered_results[:max]
    return final_results


def sort_results(torrent_list, criteria):
    return sorted(torrent_list, key=attrgetter(criteria), reverse=True)
