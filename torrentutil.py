import bencode
import hashlib
import base64
import urllib
import requests

def to_magnet(torrent_link):  
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
    return magneturi;
print to_magnet("https://yts.re/torrent/download/3FBFACC87CC7108B60BB64D5C3A38FBB8226B21E.torrent")
