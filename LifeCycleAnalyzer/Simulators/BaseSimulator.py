class BaseSimulator:

	def __init__(self, **params):
		'''Constructor method'''
		self.settings = params.pop('settings')

	def get_one_instance():
		'''Get one instance of simulation in the life cycle'''
		raise NotImplementedError ("The get_one_instance is not implemented yet")