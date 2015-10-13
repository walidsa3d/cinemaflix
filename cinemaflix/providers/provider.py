
class BaseProvider(object):

    """A base class for search providers"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'Referer': self.base_url,
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}

    def search(self, query):
        pass

    def get_top(self):
        pass
