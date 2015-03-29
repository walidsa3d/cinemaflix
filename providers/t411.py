import json
import requests
from models import Torrent

HTTP_OK = 200
API_URL = 'https://api.t411.me/%s'
USER_FILE = 'user.json'

class T411Exception(BaseException):
    pass

class T411(object):
    """ Base class for t411 interface """

    def __init__(self, username = None, password = None) :
        """ Get user credentials and authentificate it, if any credentials
        defined use token stored in user file
        """
        with open(USER_FILE) as user_file:
                self.login = json.loads(user_file.read())
                print self.login
                if 'user' not in self.login or 'pass' not in \
                        self.login:
                    raise T411Exception('Wrong data found in user file')
        user = self.login['user']
        password =self.login['pass']
        self.auth(user, password)

    def auth(self, username, password) :
        """ Authentificate user and store token """
        self.user_token = self.api_call('auth', params={'username': username, 'password': password})
        if 'error' in self.user_token:
            raise T411Exception('Error while fetching authentication token: %s'\
                    % self.user_token['error'])
        return True

    def api_call(self, method = '', params = None) :
        """ Call T411 API """
        url=API_URL % method
        headers={}
        if method != 'auth' :
            headers['Authorization']=self.user_token['token']
        req = requests.post(url,data=params,headers=headers)
        if req.status_code == requests.codes.OK:
            return req.json()
        else :
            raise T411Exception('Error while sending %s request: HTTP %s' % \
                    (method, req.status_code))

    def me(self) :
        """ Get personal informations """
        return self.call('users/profile/%s' % self._uid)
    def search(self,query):
        data=self.api_call('/torrents/search/%s?&limit=40' %query)
        torrents=[]
        print data
        for result in data['torrents']:
            t=Torrent()
            t.title=result['name']
            t.size=result['size']
            t.seeds=int(result['seeders'])
            torrents.append(t)
        return torrents

    def user(self, user_id) :
        """ Get user informations """
        return self.api_call('users/profile/%s' % user_id)

    def categories(self) :
        """ Get categories """
        return self.api_call('categories/tree')

    def terms(self) :
        """ Get terms """
        return self.api_call('terms/tree')

    def details(self, torrent_id) :
        """ Get torrent details """
        return self.api_call('torrents/details/%s' % torrent_id)

    def download(self, torrent_id) :
        """ Download a torrent """
        return self.api_call('torrents/download/%s' % torrent_id)

if __name__ == '__main__':
    print T411().search("gladiator")