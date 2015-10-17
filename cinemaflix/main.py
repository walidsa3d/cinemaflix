import inquirer
import os
import providers.searchapi as searchapi
import sys

from configobj import ConfigObj
from dateutil.parser import parse
from prettytable import PrettyTable
from sabertooth import subapi
from termcolor import colored
from utils import TorrentHandler


class TSearch(object):

    def display_results(self, torrent_list):
        for index, torrent in enumerate(torrent_list, start=1):
            index = colored(index, 'red', attrs=['blink'])
            title = colored(unicode(torrent.title), 'cyan')
            size = colored(unicode(torrent.size), 'green', attrs=['bold'])
            seeds = colored(torrent.seeds, 'white', attrs=['bold'])
            print '{} {} {} {}'.format(index, title, size, seeds)

    def display_subtitles(self, data):
        output = PrettyTable(["I", "Lang", "Release", "Date"])
        output.align = "l"
        for item in data:
            index = colored(item, 'red')
            lang = colored(data[item]['lang'], 'yellow', 'on_grey')
            dt = parse(data[item]['date'])
            date = colored(dt.strftime('%d/%m/%Y'), 'blue')
            release = colored(
                data[item]["movie"].encode('utf-8').strip(), 'green')
            output.add_row([index, lang, release, date])
        print output

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

    def show_banner(self):
        asterisk = colored('*', 'red')
        vertical_bar = colored('|', 'yellow')
        horizontal_bar = colored('-', 'blue')
        word = colored('CINEMAFLIX', 'yellow', attrs=['bold'])
        print horizontal_bar*50
        print vertical_bar+asterisk*19+word+asterisk*19+vertical_bar
        print vertical_bar+asterisk*48+vertical_bar
        print horizontal_bar*50

    def main(self):
        self.show_banner()
        # read config file
        configfile = os.path.join(os.path.dirname(__file__), 'config.ini')
        config = ConfigObj(configfile)
        player = config['player']
        min_seeds = int(config['min_seeds'])
        max_results = int(config['max_results'])
        cache_path = os.path.expanduser(config['cache_path'])
        # show categories menu
        category = self.categories_menu()
        # show site picker
        site = self.category_menu(category)
        query = raw_input('Search: ')
        if query == '':
            search_results = searchapi.get_top(site)
        else:
            search_results = searchapi.search(
                query, site, sort='seeds', seeds=min_seeds, max=max_results)
        self.display_results(search_results)
        user_input = raw_input('Pick Movie, [e]xit, [b]ack :\t')
        search_results = dict(enumerate(search_results, start=1))
        while(not user_input.isdigit() or int(user_input) > len(search_results)):
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
        handler = TorrentHandler(cache_path)
        subtitles = subapi.search(
            'opensubtitles', movie, maxnumber=10, lang='en')
        if subtitles:
            subtitles = dict(enumerate(subtitles, start=1))
            self.display_subtitles(subtitles)
            sub_choice = raw_input('Choose Subtitle:\t')
            if sub_choice not in map(str, range(1, 10)):
                print "Choice Not Available"
                return
            sub_choice = subtitles[int(sub_choice)]
            subtitle_file = subapi.download(
                'opensubtitles', sub_choice, cache_path)
            print 'Streaming ' + movie
            handler.stream(
                'peerflix', movie_url, player, subtitle=subtitle_file)
        else:
            print 'No subtitles found\n'
            streamit = raw_input('Stream movie? (y/n)\t')
            if streamit == "y":
                print 'Streaming ' + movie
                handler.stream('peerflix', movie_url, player, subtitle=None)
            else:
                return

if __name__ == '__main__':
    TSearch().main()
