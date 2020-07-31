from utils.GeneralSettings import *

class BaseDeterioration(object):

	def __init__(self):
		super().__init__()

	def predict_condition(self, previous_condition = None, age = None):
		raise NotImplementedError ("The predict_condition method is not implemented yet")

	def set_asset(self, asset):
		self.asset = asset

	def set_element(self, element):
		self.element = element