import argparse
import providers.yts as yts
import providers.kickass as kickass
import providers.tpb as tpb
import providers.nyaa as nyaa
from magneto import to_magnet
from prettytable import PrettyTable
import sys

class TSearch:  
   
    def display_results(self,torrent_list):
        results = PrettyTable(["Index","Name","Quality", "Seeds", "Size"])
        results.align["Name"] = "l" # Left align city names
        #torrs=dict(enumerate(torrent_list))
        for index,torrent in enumerate(torrent_list):
            results.add_row([index,torrent.title,torrent.quality,torrent.seeds, unicode(torrent.size)])
        print results

    def main(self):
        parser = argparse.ArgumentParser(description='A Multi-Provider Movie Search API')
        parser.add_argument('provider')
        parser.add_argument('query')
        torrents=[]
        args = parser.parse_args()
        if(args.provider=="kickass"):
            torrents=kickass.search(args.query)
        if(args.provider=="yts"):
            torrents=yts.search(args.query)
        if(args.provider=="tpb"):
            torrents=tpb.search(args.query)
        if(args.provider=="nyaa"):
            torrents=nyaa.search(args.query)
        if(args.provider=="eztv"):
            torrents=eztv.search(args.query)
        self.display_results(torrents)
        x=raw_input("Type number to choose movie or e to exit :\t")
        torrs=dict(enumerate(torrents))
        while(int(x) >= len(torrs)):
            print "Wrong number \n"
            x=raw_input("Type number to choose movie or e to exit :\t")
        if x=="e":
            sys.exit()
        else:
            print to_magnet(torrs[int(x)].torrent_url)

if __name__ == '__main__':
    TSearch().main()