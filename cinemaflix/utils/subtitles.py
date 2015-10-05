import gzip
import logging
import os
import requests
import shutil
import xmlrpclib

from utils import utils


OS_LANGS = {"en": "eng", "fr": "fre", "hu": "hun", "cs": "cze", "pl": "pol", "sk": "slo",
            "pt": "por", "pt-br": "pob", "es": "spa", "el": "ell", "ar": "ara", 'sq': 'alb',
            "hy": "arm", "ay": "ass", "bs": "bos", "bg": "bul", "ca": "cat", "zh": "chi", "hr": "hrv",
            "da": "dan", "nl": "dut", "eo": "epo", "et": "est", "fi": "fin", "gl": "glg", "ka": "geo",
            "de": "ger", "he": "heb", "hi": "hin", "is": "ice", "id": "ind", "it": "ita", "ja": "jpn",
            "kk": "kaz", "ko": "kor", "lv": "lav", "lt": "lit", "lb": "ltz", "mk": "mac", "ms": "may",
            "no": "nor", "oc": "oci", "fa": "per", "ro": "rum", "ru": "rus", "sr": "scc", "sl": "slv",
            "sv": "swe", "th": "tha", "tr": "tur", "uk": "ukr", "vi": "vie"}


class opensubtitles:

    def download_subtitle(self, subtitle, dldir):
        dldir = os.path.expanduser(dldir)
        suburl = subtitle["link"]
        videofilename = subtitle["release"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        response = requests.get(suburl, stream=True)
        with open(srtbasefilename + ".srt.gz", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        f = gzip.open(srtbasefilename + ".srt.gz")
        with open(dldir + srtbasefilename + ".srt", "w") as dump:
            dump.write(f.read())
        f.close()
        os.remove(srtbasefilename + ".srt.gz")
        return dldir + srtbasefilename + ".srt"

    def best_subtitle(self, filename, langs):
        subtitles = self.search_by_name(filename, langs)
        best_match = subtitles[0]
        maxi = 0
        for subtitle in subtitles:
            ratio = utils.compare(filename, subtitle['release'])
            if ratio > maxi:
                maxi = ratio
                best_match = subtitle
        return best_match if len(subtitles) > 0 else None

    def search_by_name(self, query, langs):
        results = self.query(query)
        return [x for x in results if x["lang"] in langs]

    def query(self, filename, imdbID=None, moviehash=None, bytesize=None, langs=None):
        '''Note: if using moviehash, bytesize is required.    '''
        log = logging.getLogger(__name__)
        log.debug('query')
        # Prepare the search
        search = {}
        sublinks = []
        if moviehash:
            search['moviehash'] = moviehash
        if imdbID:
            search['imdbid'] = imdbID
        if bytesize:
            search['moviebytesize'] = str(bytesize)
        if len(search) == 0:
            log.debug("No search term, we'll use the filename")
            search['query'] = filename
            log.debug(search['query'])

        # Login
        server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc')
        log_result = server.LogIn("", "", "eng", "periscope")
        log.debug(log_result)
        token = log_result["token"]
        results = server.SearchSubtitles(token, [search])
        sublinks = []
        if results['data']:
            log.debug(results['data'])
            for r in results['data']:
                result = {}
                result["release"] = r['SubFileName']
                result["link"] = r['SubDownloadLink']
                result["page"] = r['SubDownloadLink']
                result["lang"] = r['SubLanguageID']
                sublinks.append(result)
        try:
            server.LogOut(token)
        except:
            log.error("Open subtitles could not be contacted for logout")
        return sublinks
