import subprocess

class peerflix(object):
	"""peerflix wrapper"""
	def __init__(self):
		super(peerflix, self).__init__()
	def play(self,link,player='vlc',subtitle=None):
		peerflix_args="-d"
		command="peerflix '{}' --{} --subtitles '{}' {}".format(link,player,subtitle,peerflix_args)
		subprocess.Popen(command, shell=True) 	