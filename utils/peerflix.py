import subprocess

class peerflix(object):
	"""peerflix wrapper"""
	def __init__(self):
		super(peerflix, self).__init__()
	def play(self,link,player='vlc',subtitle=None):
		command="peerflix '{}' --{} --subtitles '{}'".format(link,player,subtitle)
		print command
		subprocess.Popen(command, shell=True) 	