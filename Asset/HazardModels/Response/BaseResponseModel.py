

class BaseResponseModel(object):

	def __init__(self):
		super().__init__()

	def get_response(self, pga=None, pgd=None, sa_long=None, sa_short = None):
		raise NotImplementedError ("get_response model is not implemented yet")