# walid.saad

from __future__ import division
import bencode
import hashlib
import base64
import requests
import math
import subprocess


class utils:

    def to_magnet(self, torrent_link):
        """converts a torrent file to a magnet link"""
        response = requests.get(torrent_link, stream=True)
        with open('tempfile.torrent', 'w') as out_file:
            out_file.write(response.content)
            out_file.close()
        torrent = open('tempfile.torrent', 'r').read()
        metadata = bencode.bdecode(torrent)
        hashcontents = bencode.bencode(metadata['info'])
        digest = hashlib.sha1(hashcontents).digest()
        b32hash = base64.b32encode(digest)
        # params = {'xt': 'urn:btih:%s' % b32hash,'dn': metadata['info']['name'],'tr': metadata['announce']}
        # paramstr = urllib.urlencode(params)
        magneturi = 'magnet:?xt=urn:btih:%s' % b32hash
        return magneturi

    def to_torrent(self, magneturi):
        pass

    @staticmethod
    def hsize(bytes):
        """converts a bytes to human-readable format"""
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        if bytes == 0:
            return "0 Byte"
        i = int(math.floor(math.log(bytes) / math.log(1024)))
        r = round(bytes / math.pow(1024, i), 2)
        return str(r) + '' + sizes[i]

    @staticmethod
    def ratio(leechs, seeds):
        return seeds/leechs if leechs != 0 else float('inf')

    def download_torrent(self, torrent_url, location):
        pass

    @staticmethod
    def play(link, player, path, subtitle=None):
        command = "peerflix '{}' --{} --subtitles '{}' -f {} -d".format(
            link, player, subtitle, path)
        subprocess.Popen(command, shell=True)
