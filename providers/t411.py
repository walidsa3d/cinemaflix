import json
import requests
from torrent import Torrent
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
        
        try :
            with open(USER_FILE) as user_file:
                self.user_credentials = json.loads(user_file.read())
                if 'uid' not in self.user_credentials or 'token' not in \
                        self.user_credentials:
                    raise T411Exception('Wrong data found in user file')
                else:
                    # we have to ask the user for its credentials and get
                    # the token from the API
                    user = raw_input('Please enter username: ')
                    password = raw_input('Please enter password: ')
                    self.auth(user, password)
        except IOError as e:
            # we have to ask the user for its credentials and get
            # the token from the API
            user = raw_input('Please enter username: ')
            password = raw_input('Please enter password: ')
            print user,password
            self.auth(user, password)
        except T411Exception as e:
            raise T411Exception(e.message)
        except Exception as e:
            raise T411Exception('Error while reading user credentials: %s.'\
                    % e.message)

    def auth(self, username, password) :
        """ Authentificate user and store token """
        self.user_credentials = self.api_call('auth', params={'username': username, 'password': password})
        if 'error' in self.user_credentials:
            raise T411Exception('Error while fetching authentication token: %s'\
                    % self.user_credentials['error'])
        #Create or update user file
        user_data = json.dumps({'uid': '%s' % self.user_credentials['uid'], 'token': '%s' % self.user_credentials['token']})
        print user_data
        with open(USER_FILE, 'w') as user_file:
             user_file.write(user_data)
        return True

    def api_call(self, method = '', params = None) :
        """ Call T411 API """
        url=API_URL % method
        headers={}
        if method != 'auth' :
            headers['Authorization']=self.user_credentials['token']
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