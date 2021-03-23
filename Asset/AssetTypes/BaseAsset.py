#Loading dependencies
import numpy as np

class BaseAsset:
	def __init__(self, ID = 11111, **kwargs):
		'''Parent object for all future assets

		::params::
		ID: the id of each asset
		settings: the general setting of the analysis
		'''
		self.ID = ID
		for key, value in kwargs.items():
			setattr(self, key, value)

		self.elements = []
		self.set_elements_util_weight()

	def set_elements_util_weight(self, weights = None):
		'''Set the elements utility
	
		This vector will be used in the optimization and life cycle analysis...
		...to calcualte the utility of an asset
		'''
		if weights is None:
			#If None: equal weight
			self.elements_util_weight = \
				np.array([1/self.settings.n_elements for _ in range(self.settings.n_elements)])
		
		elif isinstance(weights, (list, np.ndarray)):
			#If list of array: set it to the 
			if np.array(weights).ndim != 1:

				#Checking if it's one dimensional
				raise ValueError ('weights MUST be 1D np array')

			elif len(weights) != len(self.elements):
				#Checking if the length of elements and weights are equal
				raise ValueError('length of weights and elements must be equal')

			self.elements_util_weight = weights

		else:
			raise ValueError('weights MUST be None, a list or numpy array')

	def set_accumulator(self, accumulator):
		'''Set an accumulator for storing the results of simulation'''
		try:
			self.accumulator = accumulator(ID = self.ID,
										elements = self.elements,
										elements_util_weight = self.elements_util_weight,
										settings = self.settings)
		except:
			raise ValueError ("accumulator should be AccumulatorX, AccumualtorThree, or a similar accumulator")

	def refresh_age(self):
		'''refreshing age that will be used in simulators'''
		for element in self.elements:
			element.refresh_age()

	def set_mrr_model(self, mrr):
		'''Set the mrr model to the asset'''
		if not "MRR" in str(type(mrr)):
			raise ValueError ("mrr should be an instance of MRRActions")
		self.mrr_model = mrr

	def set_user_cost_model(self, model):
		'''Set the user cost model to the asset'''
		if not "UserCostModels" in str(type(model)):
			raise ValueError ("model must be a user cost model")
		model.set_asset(self)
		self.user_cost_model = model

	def set_hazard_model(self, model):
		'''Set the hazard model to the asset'''
		if not "HazardModels" in str(type(model)):
			raise ValueError ('model must be an instance of hazard models')
		self.hazard_model = model

	def add_element(self, element):
		'''adding elements to the asset'''
		if not "Elements" in str(type(element)):
			raise ValueError ('element must be an instance of elements')
		self.elements.append(element)

	def set_traffic_info(self, **kwargs):
		'''Set the traffic information of the bridge'''
		for key, value in kwargs.items():
			setattr(self, key, value)

	def set_seismic_info(self, **kwargs):
		'''Set the seismic information of the bridge'''
		for key, value in kwargs.items():
			setattr(self, key, value)

	def set_replacement_value_model(self, model = None):
		'''Set the replacement value model'''
		self.replacement_value = model

	def __repr__(self):
		'''String representation of the asset'''
		return f"Asset-{self.ID}"

	