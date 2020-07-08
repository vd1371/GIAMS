

class BaseElement(object):

	def __init__(self, name = None, initial_condition = None, age = 0):
		super().__init__()
		
		self.name = name
		self.initial_condition = initial_condition
		self.age = age
		self.conditions_in_horizon = []

	def refresh(self):
		self.conditions_in_horizon = []

	def set_age(self, new_age):
		self.age = new_age

	def append_next_condition(self, con):
		self.conditions_in_horizon.append(con)

	def set_condition_rating_model(self, model):
		self.conditon_rating_model = model

	def set_deterioration_model(self, model):
		self.deterioration_model = model

	def set_maintenance_cost_model(self, model):
		self.maintenance_cost_model = model

	def set_rehabilitation_cost_model(self, model):
		self.rehabilitation_cost_model = model

	def set_reconstruction_cost_model(self, model):
		self.reconstruction_cost_model = model

	def set_utility_model(self, model):
		self.set_utility_model = model
	
	def __repr__(self):
		return f"{self.name}-CR:{self.initial_condition}-Age:{self.age}"

