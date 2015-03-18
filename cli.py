import providers.yts as yts
import providers.kickass as kickass
import providers.tpb as tpb
import providers.nyaa as nyaa
import providers.limetorrents as lime
from providers.t411 import T411 as t411
import providers.cpabsien as cpabsien
from magneto import to_magnet
import sys
import inquirer
from termcolor import colored
from operator import attrgetter

class TSearch:  
   
    def display_results(self, torrent_list):
        for index,torrent in enumerate(torrent_list):
            index=colored(index,'red',attrs=['blink'])
            title=colored(unicode(torrent.title),'cyan')
            size=colored(unicode(torrent.size),'green',attrs=['bold'])
            seeds=colored(torrent.seeds,'white',attrs=['bold'])
            print index+" "+title+" "+size+" "+seeds

    def sort_results(self,torrent_list,criteria):
        return sorted(torrent_list,key=attrgetter(criteria),reverse=True)
    def filter_results(self,torrent_list,criteria):
        return [x for x in torrent_list if x['seeds']>=100]
    def main(self):
        sites=['Yts','Kickass','ThePirateBay','LimeTorrents',"T411",'Cpabsien']
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
        if(site=="cpabsien"):
            torrents=cpabsien.search(query)
        if(site=="t411"):
            torrents=t411().search(query)
        self.display_results(self.sort_results(torrents,'seeds'))
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