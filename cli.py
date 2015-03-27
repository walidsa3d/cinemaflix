import sys
import inquirer
from termcolor import colored
import providers.searchapi as api
from utils.peerflix import peerflix

class TSearch:  
   
    def display_results(self, torrent_list):
        for index,torrent in enumerate(torrent_list):
            index=colored(index,'red',attrs=['blink'])
            title=colored(unicode(torrent.title),'cyan')
            size=colored(unicode(torrent.size),'green',attrs=['bold'])
            seeds=colored(torrent.seeds,'white',attrs=['bold'])
            print index+" "+title+" "+size+" "+seeds

    def main(self):
        sites=['Yts','Kickass','ThePirateBay','OldPirateBay','LimeTorrents',"T411",'Cpabsien','Strike']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        query=raw_input("Search Movie: ")
        while(query==""):
            query=raw_input("Search Movie: ")
        torrents=api.search(query,site)
        self.display_results(api.sort_results(torrents,'seeds'))
        x=raw_input("Type index to choose movie or e to exit :\t")
        torrs=dict(enumerate(torrents))
        while(int(x) >= len(torrs)):
            print "Wrong number \n"
            x=raw_input("Type number to choose movie or e to exit :\t")
        if x=="e":
            sys.exit()
        else:
            peerflix().play(torrs[int(x)].torrent_url)
        
if __name__ == '__main__':
    TSearch().main()