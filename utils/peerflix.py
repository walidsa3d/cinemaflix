import subprocess

class peerflix(object):
	"""peerflix wrapper"""
	def __init__(self):
		super(peerflix, self).__init__()
	def play(self,link,player,path,subtitle=None):
		command="peerflix '{}' --{} --subtitles '{}' -f {} -d".format(link,player,subtitle,path)
		subprocess.Popen(command, shell=True) 	