import argparse
import yts
import kickass
import tpb
from prettytable import PrettyTable
from torrentutil import to_magnet

class TSearch:  
   
    def display_torrents(self,torrent_list):
        results = PrettyTable(["Index","Name","Quality", "Seeds", "Size"])
        results.align["Name"] = "l" # Left align city names
        #torrs=dict(enumerate(torrent_list))
        for index,torrent in enumerate(torrent_list):
            results.add_row([index,torrent.title,torrent.quality,torrent.seeds, str(torrent.size)])
        print results



    def main(self):
        parser = argparse.ArgumentParser(description='A Multi-Provider Torrent Search API')
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
        self.display_torrents(torrents)
        x=raw_input("choose movie :\t")
        torrs=dict(enumerate(torrents))
        print to_magnet(torrs[int(x)].torrent_url)

if __name__ == '__main__':
    TSearch().main()