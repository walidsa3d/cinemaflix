
from __future__ import division

import base64
import bencode
import difflib
import hashlib
import math
import os
import requests
import subprocess

class utils(object):

    def __init__(self):
        pass

    @staticmethod
    def to_magnet(torrent_link):
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
        magneturi = 'magnet:?xt=urn:btih:%s' % b32hash
        return magneturi

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
        return seeds / leechs if leechs != 0 else float('inf')

    def download_torrent(self, torrent_url, location):
        pass

    @staticmethod
    def play(link, player, path, subtitle=None):
        command = "peerflix '{}' --{} --subtitles '{}' -f {} -d".format(
            link, player, subtitle, path)
        print command
        subprocess.Popen(command, shell=True)

    @staticmethod
    def playvid(link):
        command = "youstream {} --mpv".format(link)
        subprocess.Popen(command, shell=True)

    @staticmethod
    def check_yt(youtube_link):
        url = "http://www.youtube.com/oembed?url={}&format=json".format(
            youtube_link)
        response = requests.head(url)
        return response.status_code != 404

    @staticmethod
    def parse_magnet(magnet_link):
        pass

    @staticmethod
    def compare(movie, sub):
        ratio = 0
        seq = difflib.SequenceMatcher(None, movie, sub)
        ratio = ratio + seq.ratio()
        return ratio
    @staticmethod
    def is_installed(cmd):
        inst = lambda x: any(os.access(os.path.join(path, x), os.X_OK) for path
                             in os.environ["PATH"].split(os.pathsep))
        return inst(cmd)