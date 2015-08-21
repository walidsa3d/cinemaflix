# walid.saad

from yts import yts
from kickass import kickass
from tpb import tpb
from nyaa import nyaa
import limetorrents as lime
from t411 import t411
from cpabsien import cpabsien
from strike import strike
from eztv import eztv
from redditmovies import redditmovies
from redditdocus import redditdocus
from watchseries import watchseries
from operator import attrgetter
import re


def search(query, provider, sort=None, seeds=0, max=0):
    results = []
    sorts = ['seeds', 'size']
    if(provider == "kickass"):
        results = kickass().search(query)
    if(provider == "redditmovies"):
        results = redditmovies().search(query)
    if(provider == "redditdocus"):
        results = redditdocus().search(query)
    if(provider == "watchseries"):
        results = watchseries().search(query)
    if(provider == "yts"):
        results = yts().search(query)
    if(provider == "thepiratebay"):
        results = tpb().search(query)
    if(provider == "limetorrents"):
        results = lime.search(query)
    if(provider == "cpabsien"):
        results = cpabsien().search(query)
    if(provider == "t411"):
        results = t411().search(query)
    if(provider == "strike"):
        results = strike().search(query)
    if(provider == "nyaa"):
        results = nyaa().search(query)
    if(provider == "eztv"):
        results = eztv().search(query)
    filtered_results = [x for x in sort_results(
        results, sort) if x.seeds >= seeds] if sort in sorts else [x for x in results if x.seeds >= seeds]
    final_results = filtered_results[:max]
    return final_results


def sort_results(torrent_list, criteria):
    return sorted(torrent_list, key=attrgetter(criteria), reverse=True)
