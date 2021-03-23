'''Bridge asset class'''
from .BaseAsset import BaseAsset

class Bridge(BaseAsset):

	def __init__(self, ID = 11111, **kwargs):
		super().__init__(ID, **kwargs)
	