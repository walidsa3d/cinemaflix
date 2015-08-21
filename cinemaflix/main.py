import sys
import inquirer
from termcolor import colored
import providers.searchapi as api
from utils.utils import utils
from utils.subtitles import opensubtitles as opensubs
from configobj import ConfigObj
import os


class TSearch:

    def display_results(self, torrent_list):
        for index, torrent in enumerate(torrent_list):
            index = colored(index, 'red', attrs=['blink'])
            title = colored(unicode(torrent.title), 'cyan')
            size = colored(unicode(torrent.size), 'green', attrs=['bold'])
            seeds = colored(torrent.seeds, 'white', attrs=['bold'])
            print index + " " + title + " " + size + " " + seeds

    def categories_menu(self):
        categories = ['Movies', 'Series', 'Anime']
        subs = [
            inquirer.List('category',
                          message="Choose a Category",
                          choices=categories,
                          ),
        ]
        category = inquirer.prompt(subs)['category'].lower()
        return category

    def movies_menu(self):
        sites = ['Yts', 'Kickass', 'ThePirateBay',
                 "T411", 'Cpabsien', 'Strike', 'RedditMovies',"RedditDocus"]
        subs = [
            inquirer.List('site',
                          message="Choose a Provider",
                          choices=sites,
                          ),
        ]
        site = inquirer.prompt(subs)['site'].lower()
        return site

    def series_menu(self):
        sites = ['EZTV']
        subs = [
            inquirer.List('site',
                          message="Choose a Provider",
                          choices=sites,
                          ),
        ]
        site = inquirer.prompt(subs)['site'].lower()
        return site

    def anime_menu(self):
        sites = ['Nyaa']
        subs = [
            inquirer.List('site',
                          message="Choose a Provider",
                          choices=sites,
                          ),
        ]
        site = inquirer.prompt(subs)['site'].lower()
        return site

    def main(self):
        config = ConfigObj("config.ini")
        player = config['player']
        min_seeds = int(config['min_seeds'])
        max_results = int(config['max_results'])
        cache_path = config['cache_path']
        category = self.categories_menu()
        if category == "movies":
            site = self.movies_menu()
        if category == "series":
            site = self.series_menu()
        if category == "anime":
            site = self.anime_menu()
        query = raw_input("Search: ")
        while(query == ""):
            query = raw_input("Search: ")
        search_results = api.search(
            query, site, sort='seeds', seeds=min_seeds, max=max_results)
        self.display_results(search_results)
        user_input = raw_input("Pick Movie, [e]xit, [b]ack :\t")
        search_results = dict(enumerate(search_results))
        while(not user_input.isdigit() or int(user_input) >= len(search_results)):
            if user_input == "e":
                sys.exit()
            elif user_input == "b":
                os.system('clear')
                self.main()
            else:
                user_input = raw_input(
                    "Wrong Choice \nPick Movie, [e]xit, [b]ack :\t")
        movie = search_results[int(user_input)].title
        movie_url = search_results[int(user_input)].torrent_url
        subtitle = opensubs().best_subtitle(movie, ["eng"])
        if subtitle is not None:
            print "Subtitles found!\nDownloading.."
            subtitle_file = opensubs().download_subtitle(subtitle, cache_path)
            print "Streaming " + movie
            #utils().playvid(movie_url)
            utils.play(movie_url, player, cache_path, subtitle=subtitle_file)
        else:
            print "No subtitles found"
            print "Streaming " + movie
            # utils.play(movie_url, player, cache_path)
            utils().playvid(movie_url)

if __name__ == '__main__':
    TSearch().main()
