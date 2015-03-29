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
    def cat_chooser(self):
        categories=['Movies','Series']
        subs = [
              inquirer.List('category',
                            message="Choose a Category",
                            choices=categories,
                        ),
            ]
        category = inquirer.prompt(subs)['category'].lower()
        return category
    def movie_site_chooser(self):
        sites=['Yts','Kickass','ThePirateBay','OldPirateBay','LimeTorrents',"T411",'Cpabsien','Strike']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        return site
    def series_site_chooser(self):
        sites=['EZTV','Nyaa']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        return site

    def main(self):
        category=self.cat_chooser()
        if category=="movies":
            site=self.movie_site_chooser()
        if category=="series" :
            site=self.series_site_chooser()
        query=raw_input("Search: ")
        while(query==""):
            query=raw_input("Search: ")
        torrents=api.search(query,site)
        self.display_results(api.sort_results(torrents,'seeds'))
        x=raw_input("Pick Movie Number Or Type e To Exit :\t")
        torrs=dict(enumerate(torrents))
        while(int(x) >= len(torrs)):
            print "Wrong number \n"
            x=raw_input("Type number to choose movie or e to exit :\t")
        if x=="e":
            sys.exit()
        else:
            movie=torrs[int(x)].title
            movie_url=torrs[int(x)].torrent_url
            subtitle=opensubs().best_subtitle(movie, ["eng"])
            subtitle_file=opensubs().download_subtitle(subtitle,"/tmp/")
            peerflix().play(movie_url,subtitle=subtitle_file)
        
if __name__ == '__main__':
    TSearch().main()