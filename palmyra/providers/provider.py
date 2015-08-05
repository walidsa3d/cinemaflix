

class BaseProvider:
	"""A base class for search providers"""	
	def __init__(self):
		self.headers=[""]

	def search(self,query):
		pass
	