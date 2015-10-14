import json
import os
import re
import requests

from models import Torrent
from operator import itemgetter
from provider import BaseProvider


class Eztv(BaseProvider):

    def __init__(self, base_url):
        super(Eztv, self).__init__(base_url)
        self.shows = []
        self.shows_cache_path = os.path.join(
            os.path.dirname(__file__), 'cache.json')

    def _get_shows(self):
        shows_url = self.base_url+"shows/"
        data = requests.get(shows_url).json()
        shows = []
        for url in [shows_url+unicode(x) for x in xrange(1, 16)]:
            data = requests.get(url).json()
            for show in data:
                shows.append({'id': show['imdb_id'], 'title': show['title']})
        return shows

    def _search_show(self, query):
        with open(self.shows_cache_path, "r") as f:
            shows = json.load(f)
        result = None
        for show in shows:
            match = query.lower() == show['title'].lower()
            if match:
                result = show
                break
        return result

    def _cache_shows(self):
        shows = self._get_shows()
        with open(self.shows_cache_path, 'w') as f:
            f.write(json.dumps(shows))

    def _get_show_episodes(self, show_id):
        show_url = self.base_url+"show/"+show_id
        data = requests.get(show_url).json()
        episodes = []
        for episode in data['episodes']:
            episodes.append({'num': episode['episode'], 'season': episode['season'], 'title': episode[
                            'title'], 'torrent_url': episode['torrents']["0"]['url'], 'seeds': episode['torrents']["0"]['seeds']})
        episodes = sorted(episodes, key=lambda k: (k['season'], k['num']))
        return episodes

    def _search_episode(self, show, season=None, episode=None):
        torrents = []
        all_episodes = self._get_show_episodes(show['id'])
        if episode is not None:
            for ep in all_episodes:
                if season == ep['season'] and ep['num'] == episode:
                    t = Torrent()
                    t.title = show['title']+'.'+'S' + \
                        str(season)+'E'+str(ep['num'])+':'+ep['title']
                    t.torrent_url = ep['torrent_url']
                    t.seeds = ep['seeds']
                    torrents.append(t)
                    break
        return torrents

    def _get_season_episodes(self, show, season):
        torrents = []
        all_episodes = self._get_show_episodes(show['id'])
        for ep in all_episodes:
            if season == ep['season']:
                t = Torrent()
                t.title = show['title']+'.'+'S' + \
                    str(season)+'E'+str(ep['num'])+':'+ep['title']
                t.torrent_url = ep['torrent_url']
                t.seeds = ep['seeds']
                torrents.append(t)
        return torrents

    def _get_latest(self, show):
        torrents = []
        all_episodes = self._get_show_episodes(show['id'])
        sorted_episodes = sorted(
            all_episodes, key=itemgetter('season', 'num'), reverse=True)
        last_ep = {k: str(v) for k, v in sorted_episodes[0].iteritems()}
        t = Torrent()
        t.title = show['title']+'.'+'S' + \
            last_ep['season']+'E'+last_ep['num']+':'+last_ep['title']
        t.torrent_url = last_ep['torrent_url']
        t.seeds = int(last_ep['seeds'])
        torrents.append(t)
        return torrents

    def _query(self, showname, season=None, episode=None, latest=False):
        show = self._search_show(showname)
        if latest:
            torrents = self._get_latest(show)
        elif episode is None:
            season = int(season)
            torrents = self._get_season_episodes(show, season)
        else:
            season = int(season)
            episode = int(episode)
            torrents = self._search_episode(
                show, season, episode)
        return torrents

    def search(self, query):
        results = []
        ep_re = re.compile(r"(([a-zA-Z]+\s*)+)(\s[0-9]+\s[0-9]+)$")
        season_re = re.compile(r"(([a-zA-Z]+\s*)+)(\s[0-9]+)$")
        lastest_re = re.compile(r"(([a-zA-Z]+\s*)+)(latest)$")
        ep_match = ep_re.match(query)
        season_match = season_re.match(query)
        latest_match = lastest_re.match(query)
        if ep_match:
            show = ep_match.group(1)
            season = ep_match.group(3).strip().split(' ')[0]
            episode = ep_match.group(3).strip().split(' ')[1]
            results = self._query(show, season, episode)
        elif season_match:
            show = season_match.group(1)
            season = season_match.group(3).strip().split(' ')[0]
            results = self._query(show, season)
        elif latest_match:
            show = latest_match.group(1).strip()
            results = self._query(show, latest=True)
        else:
            print 'Badly Formatted Query'
        return results

    def get_top(self):
        return []
