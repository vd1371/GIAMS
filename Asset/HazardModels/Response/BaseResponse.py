class BaseResponse(object):

	def __init__(self, asset):
		super().__init__()
		'''Parent class for all response models'''
		self.asset = asset

	def get(self, **kwargs):
		raise NotImplementedError ("get_response model is not implemented yet")
