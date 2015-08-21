import praw
from models import Torrent
from provider import BaseProvider
from utils import utils


class redditdocus(BaseProvider):

    def __init__(self):
        self.subs = ["Documentaries", "sciencedocumentaries"]

    def search(self, query):
        r = praw.Reddit(user_agent='lol')
        movies = []
        for sub in self.subs:
            posts = r.search(query, subreddit=sub,
                             sort=None, syntax=None, period=None, limit=100)
            for post in posts:
                if 'youtube.com' in post.url and utils.check_yt(post.url):
                    t = Torrent()
                    t.title = post.title.split('|')[0]
                    t.torrent_url = post.url
                    t.size = ""
                    t.seeds = 100
                    movies.append(t)
        return movies
