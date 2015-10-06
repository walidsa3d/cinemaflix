
from __future__ import division

import base64
import bencode
import difflib
import hashlib
import math
import requests


class utils(object):

    def __init__(self):
        pass

    @staticmethod
    def to_magnet(torrent_link):
        """converts a torrent file to a magnet link"""
        response = requests.get(torrent_link)
        with open('tempfile.torrent', 'w') as out_file:
            out_file.write(response.content)
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
    def parse_magnet(magnet_link):
        pass

    @staticmethod
    def compare(movie, sub):
        ratio = 0
        seq = difflib.SequenceMatcher(None, movie, sub)
        ratio = ratio + seq.ratio()
        return ratio
