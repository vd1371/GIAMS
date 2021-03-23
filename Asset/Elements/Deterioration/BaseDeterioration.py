from utils.GeneralSettings import *

class BaseDeterioration(object):
	'''Parent class of all future deterioration model'''
	def __init__(self):
		super().__init__()

	def predict_condition(self):
		'''To predict the condition rating after one time step given some information'''
		raise NotImplementedError ("The predict_condition method is not implemented yet")

	def set_asset(self, asset):
		self.asset = asset

	def set_element(self, element):
		self.element = element