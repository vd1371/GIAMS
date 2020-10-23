'''
This is the main asset class
'''
import numpy as np

from utils.GeneralSettings import GenSet
from utils.PredictiveModels.Linear import Linear

class Bridge(GenSet):

	def __init__(self, ID = 11111, **kwargs):
		super().__init__()
		self.ID = ID

		for key, value in kwargs.items():
			setattr(self, key, value)

		self.elements = []
		self.elements_util_weight = np.array([1/self.n_elements for _ in range(self.n_elements)])

	def set_accumulator(self, accumulator):
		self.accumulator = accumulator(self.ID, self.elements, self.elements_util_weight)

	def refresh(self):
		for element in self.elements:
			element.refresh()

	def set_traffic_info(self, road_class = 'NHS',
								ADT = 1000,
								truck_percentage = 4,
								detour_length = 20):

		self.road_class = road_class
		self.ADT = ADT
		self.truck_percentage = truck_percentage
		self.detour_length = detour_length

	def set_seismic_info(self, hazus_class= None,
								site_class = 'A',
								skew_angle = 0,
								n_spans = 3):
	
		self.hazus_class = hazus_class
		self.site_class = site_class
		self.skew_angle = skew_angle
		self.n_spans = n_spans

	def set_mrr_model(self, mrr):
		self.mrr_model = mrr

	def set_user_cost_model(self, model):
		model.set_asset(self)
		self.user_cost_model = model

	def set_hazard_model(self, model):
		self.hazard_model = model

	def set_replacement_value_model(self, model = None, hazus_default = True):
		
		if hazus_default:
			# Based on Hazus
			if self.hazus_class in  ['HWB1', 'HWB2']: 
				val = 20
			elif self.hazus_class in ['HWB8', 'HWB9', 'HWB10', 'HWB11', 'HWB15', 'HWB16', 'HWB20', 'HWB21', 'HWB22', 'HWB23', 'HWB26', 'HWB27']:
				val = 5
			else:
				val =1
			self.replacement_value = Linear(val, 0)

		else:
			self.replacement_value = model

	def add_element(self, element):
		self.elements.append(element)
		
	def __repr__(self):
		return f"Bridge-{self.ID}"

	