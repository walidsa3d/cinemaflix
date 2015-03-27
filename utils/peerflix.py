import subprocess

class peerflix(object):
	"""peerflix wrapper"""
	def __init__(self):
		super(peerflix, self).__init__()
	def play(self,link,player='vlc'):
		command='peerflix {} --{}'.format(link,player)
		subprocess.Popen(command, shell=True) 	