
from constants import *
from cpasbien import Cpasbien
from eztv import Eztv
from kickass import Kickass
from nyaa import Nyaa
from operator import attrgetter
from rarbg import Rarbg
from strike import Strike
from tpb import TPB
from yts import YTS

providers = {
    "kickass": Kickass(KICKASS_URL),
    "rarbg": Rarbg(RARBG_URL),
    "yts": YTS(YTS_URL),
    "thepiratebay": TPB(TPB_URL),
    "cpasbien": Cpasbien(CPABSIEN_URL),
    "strike": Strike(STRIKE_URL),
    "nyaa": Nyaa(NYAA_URL),
    "eztv": Eztv(EZTV_URL)
}


def search(query, provider, sort=None, seeds=0, max=0):
    sorts = ['seeds', 'size']
    results = providers.get(provider, 'tpb').search(query)
    sorted_results = _sort_results(results, sort) if sort in sorts else results
    filtered_results = filter(lambda x: x.seeds >= seeds, sorted_results)
    final_results = filtered_results[:max]
    return final_results


def _sort_results(torrent_list, criteria):
    return sorted(torrent_list, key=attrgetter(criteria), reverse=True)


def get_top(provider):
    results = providers.get(provider, 'tpb').get_top()
    return results
