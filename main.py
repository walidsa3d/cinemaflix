import sys
import inquirer
from termcolor import colored
import providers.searchapi as api
from utils.peerflix import peerflix
from utils.subtitles import opensubtitles as opensubs

class TSearch:  
   
    def display_results(self, torrent_list):
        for index,torrent in enumerate(torrent_list):
            index=colored(index,'red',attrs=['blink'])
            title=colored(unicode(torrent.title),'cyan')
            size=colored(unicode(torrent.size),'green',attrs=['bold'])
            seeds=colored(torrent.seeds,'white',attrs=['bold'])
            print index+" "+title+" "+size+" "+seeds
    def categories_menu(self):
        categories=['Movies','Series','Anime']
        subs = [
              inquirer.List('category',
                            message="Choose a Category",
                            choices=categories,
                        ),
            ]
        category = inquirer.prompt(subs)['category'].lower()
        return category
    def movies_menu(self):
        sites=['Yts','Kickass','ThePirateBay','OldPirateBay','LimeTorrents',"T411",'Cpabsien','Strike']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        return site
    def series_menu(self):
        sites=['EZTV']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        return site
    def anime_menu(self):
        sites=['Nyaa']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        return site

    def main(self):
        category=self.categories_menu()
        if category=="movies":
            site=self.movies_menu()
        if category=="series" :
            site=self.series_menu()
        if category=="anime" :
            site=self.anime_menu()
        query=raw_input("Search: ")
        while(query==""):
            query=raw_input("Search: ")
        search_results=api.search(query,site)
        self.display_results(api.sort_results(search_results,'seeds'))
        x=raw_input("Pick Movie Number, Type [e] To Exit, [b] to go back :\t")
        search_results=dict(enumerate(search_results))
        if x=="e":
            sys.exit()
        elif x=="b":
            self.main()
        while(int(x) >= len(search_results)):
            print "Wrong number \n"
            x=raw_input("Pick movie, e to exit, b to go back :\t")       
        else:
            movie=search_results[int(x)].title
            movie_url=search_results[int(x)].torrent_url
            subtitle=opensubs().best_subtitle(movie, ["eng"])
            subtitle_file=opensubs().download_subtitle(subtitle,"/tmp/")
            peerflix().play(movie_url,subtitle=subtitle_file)
        
if __name__ == '__main__':
    TSearch().main()