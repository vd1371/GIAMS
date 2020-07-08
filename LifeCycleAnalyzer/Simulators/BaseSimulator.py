'''
The base class of the simulator
'''
from utils.GeneralSettings import GenSet

class BaseSimulator(GenSet):

	def __init__(self):
		super().__init__()

	def get_one_instance():
		return 0