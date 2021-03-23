'''Building Class'''
from .BaseAsset import BaseAsset

class Building(BaseAsset):

	def __init__(self, ID = 11111, **kwargs):
		super().__init__(ID, **kwargs)

	