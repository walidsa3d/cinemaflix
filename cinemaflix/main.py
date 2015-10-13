import inquirer
import os
import providers.searchapi as api
import sys

from utils import TorrentHandler


from configobj import ConfigObj
from termcolor import colored
from utils import opensubtitles as opensubs


class TSearch(object):

    def display_results(self, torrent_list):
        for index, torrent in enumerate(torrent_list, start=1):
            index = colored(index, 'red', attrs=['blink'])
            title = colored(unicode(torrent.title), 'cyan')
            size = colored(unicode(torrent.size), 'green', attrs=['bold'])
            seeds = colored(torrent.seeds, 'white', attrs=['bold'])
            print '{} {} {} {}'.format(index, title, size, seeds)

    def categories_menu(self):
        categories = ['Movies', 'Series', 'Anime']
        subs = [
            inquirer.List('category',
                          message='Choose a Category',
                          choices=categories,
                          ),
        ]
        category = inquirer.prompt(subs)['category'].lower()
        return category

    def category_menu(self, category):
        movie_sites = ['Yts', 'Kickass', 'ThePirateBay', 'Rarbg',
                       'Cpasbien', 'Strike']
        series_sites = ['EZTV']
        anime_sites = ['Nyaa']
        sites = {'movies': movie_sites,
                 'series': series_sites,
                 'anime': anime_sites
                 }.get(category, None)
        subs = [
            inquirer.List('site',
                          message='Choose a Provider',
                          choices=sites,
                          ),
        ]
        site = inquirer.prompt(subs)['site'].lower()
        return site

    def main(self):
        configfile = os.path.join(os.path.dirname(__file__), 'config.ini')
        config = ConfigObj(configfile)
        player = config['player']
        min_seeds = int(config['min_seeds'])
        max_results = int(config['max_results'])
        cache_path = config['cache_path']
        category = self.categories_menu()
        site = self.category_menu(category)
        query = raw_input('Search: ')
        if query == '':
            search_results = api.get_top(site)
        else:
            search_results = api.search(
                query, site, sort='seeds', seeds=min_seeds, max=max_results)
        self.display_results(search_results)
        user_input = raw_input('Pick Movie, [e]xit, [b]ack :\t')
        search_results = dict(enumerate(search_results))
        while(not user_input.isdigit() or int(user_input) >= len(search_results)):
            if user_input == 'e':
                sys.exit()
            elif user_input == 'b':
                os.system('clear')
                self.main()
            else:
                user_input = raw_input(
                    'Wrong Choice \nPick Movie, [e]xit, [b]ack :\t')
        movie = search_results[int(user_input)].title
        movie_url = search_results[int(user_input)].torrent_url
        subtitle = opensubs().best_subtitle(movie, ['eng'])
        handler = TorrentHandler(cache_path)
        if subtitle is not None:
            print 'Subtitles found!\nDownloading..'
            subtitle_file = opensubs().download_subtitle(subtitle, cache_path)
            print 'Streaming ' + movie
            handler.stream(
                'peerflix', movie_url, player, subtitle=subtitle_file)
        else:
            print 'No subtitles found'
            print 'Streaming ' + movie
            handler.stream('peerflix', movie_url, player, subtitle=None)

if __name__ == '__main__':
    TSearch().main()
