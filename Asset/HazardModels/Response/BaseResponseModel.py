

class BaseResponseModel(object):

	def __init__(self, asset):
		super().__init__()
		self.asset = asset

	def get(self, pga=None, pgd=None, sa_long=None, sa_short = None):
		raise NotImplementedError ("get_response model is not implemented yet")
