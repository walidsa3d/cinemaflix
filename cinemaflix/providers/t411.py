import json
import requests
from models import Torrent
from provider import BaseProvider

class T411(BaseProvider):
    def __init__(self,base_url, username = None, password = None) :
        super(T411, self).__init__(base_url)
        self.base_url=base_url
        with open(USER_FILE) as f:
                self.login = json.load(f)
                if any('user','pass') not in self.login:
                    raise Exception('Wrong data found in user file')
        user,password = self.login['user'],self.login['pass']
        self.auth(user, password)

    def auth(self, username, password) :
        """ Authentificate user and store token """
        self.user_token = self._api_call('auth', params={'username': username, 'password': password})
        if 'error' in self.user_token:
            raise Exception('Error while fetching authentication token: %s'\
                    % self.user_token['error'])
        return True

    def _api_call(self, method = '', params = None) :
        """ Call T411 API """
        url=self.base_url
        if method != 'auth' :
            self.headers['Authorization']=self.user_token['token']
        req = requests.post(url,data=params,headers=self.headers).json()
        return req

    def search(self,query):
        data=self._api_call('/torrents/search/%s?&limit=40' %query)
        torrents=[]
        print data
        for result in data['torrents']:
            t=Torrent()
            t.title=result['name']
            t.size=result['size']
            t.seeds=int(result['seeders'])
            torrents.append(t)
        return torrents

    def details(self, torrent_id) :
        """ Get torrent details """
        return self._api_call('torrents/details/%s' % torrent_id)
