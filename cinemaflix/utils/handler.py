import os
import subprocess


class ResourceNotFoundException(Exception):
    pass


class TorrentHandler(object):

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.players = ['vlc', 'mpv', 'mplayer']

    def stream_with_peerflix(self, link, player, subtitle=None):
        if player not in self.players:
            raise ResourceNotFoundException('Player Not Found')
        if not self.which('peerflix'):
            raise ResourceNotFoundException('Peerflix Not Found')
        command = 'peerflix "{}" --{} -f {} -d'.format(
            link, player, self.cache_path)
        if subtitle is not None:
            command += ' --subtitles "%s"' % subtitle
        subprocess.Popen(command, shell=True)

    def stream_with_webtorrent(self, link, player, subtitle=None):
        if player not in self.players:
            raise ResourceNotFoundException('Player Not Found')
        if not self.which('webtorrent'):
            raise ResourceNotFoundException('WebTorrent Not Found')
        command = 'webtorrent "{}" --{} -o {}'.format(
            link, player, self.cache_path)
        if subtitle is not None:
            command = command + ' --subtitles "%s"' % subtitle
        subprocess.Popen(command)

    def stream(self, handler, link, player, subtitle=None):
        if handler == 'peerflix':
            self.stream_with_peerflix(link, player, subtitle)
        elif handler == 'webtorrent':
            self.stream_with_webtorrent(link, player, subtitle)
        else:
            raise ResourceNotFoundException('handler not supported')

    @staticmethod
    def which(cmd):
        inst = lambda x: any(os.access(os.path.join(path, x), os.X_OK) for path
                             in os.environ["PATH"].split(os.pathsep))
        return inst(cmd)
