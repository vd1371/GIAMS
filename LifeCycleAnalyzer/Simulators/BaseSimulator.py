class BaseSimulator:

	def __init__(self, **params):
		self.settings = params.pop('settings')

	def get_one_instance():
		raise NotImplementedError ("The get_one_instance is not implemented yet")