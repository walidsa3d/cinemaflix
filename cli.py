import argparse
import providers.yts as yts
import providers.kickass as kickass
import providers.tpb as tpb
import providers.nyaa as nyaa
import providers.limetorrents as lime
from magneto import to_magnet
from prettytable import PrettyTable
from painter import paint
import sys
import inquirer
from termcolor import colored
from operator import attrgetter
class TSearch:  
   
    def display(self, torrent_list):
        for index,torrent in enumerate(torrent_list):
            index=colored(index,'red',attrs=['blink'])
            title=colored(unicode(torrent.title),'cyan')
            size=colored(unicode(torrent.size),'green',attrs=['bold'])
            seeds=colored(torrent.seeds,'white',attrs=['bold'])
            print index+" "+title+" "+size+" "+seeds

    def sort_torrents(self,torrent_list,criteria):
        return sorted(torrent_list,key=attrgetter(criteria),reverse=True)
    def filter_torrents(self,torrent_list):
        return [x for x in torrent_list if x['seeds']>=100]
    def main(self):
        sites=['Yts','Kickass','ThePirateBay','LimeTorrents']
        subs = [
              inquirer.List('site',
                            message="Choose a Provider",
                            choices=sites,
                        ),
            ]
        site = inquirer.prompt(subs)['site'].lower()
        query=raw_input("Search Movie: ")
        torrents=[]
        if(site=="kickass"):
            torrents=kickass.search(query)
        if(site=="yts"):
            torrents=yts.search(query)
        if(site=="thepiratebay"):
            torrents=tpb.search(query)
        if(site=="limetorrents"):
            torrents=lime.search(query)
        self.display(self.sort_torrents(torrents,'seeds'))
        x=raw_input("Type index to choose movie or e to exit :\t")
        torrs=dict(enumerate(torrents))
        while(int(x) >= len(torrs)):
            print "Wrong number \n"
            x=raw_input("Type number to choose movie or e to exit :\t")
        if x=="e":
            sys.exit()
        else:
            print torrs[int(x)].torrent_url
if __name__ == '__main__':
    TSearch().main()