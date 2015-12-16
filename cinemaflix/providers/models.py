class Torrent(object):

    def __init__(self):
        self.title = ''
        self.torrent_url = ''
        self.seeds = 0
        self.size = ''

    def __eq__(self, other):
        return self.title == other.title

    def __repr__(self):
        return '(%s, %s,%s,%s)' % (
            self.torrent_url,
            self.title,
            repr(self.seeds),
            self.size
        )

    def __str__(self):
        return self.title
