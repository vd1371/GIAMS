class BaseHazard(object):
	
	def __init__(self):
		super().__init__()
		'''Parent class for all future hazard generators'''

	def set_magnitude_distribution(self):
		raise ("set_magnitude_distribution is not implemented yet")

	def generate_one_instance(self):
		raise ("generate_one_instance is not implemented yet")

	def generate_one_lifecycle(self):
		raise ("generate_one_lifecycle is not implemented yet")