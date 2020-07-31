import numpy as np
from scipy.stats import norm
from copy import deepcopy

from .BaseResponse import BaseResponse

MEDIAN = 0 # It's just an index, to make it more clear to read
BETA = 1 # It's just an index, to make it more clear to read

class HazusBridgeResponse(BaseResponseModel):

	def __init__(self, asset):
		super().__init__(asset)
		
		self.damage_state_dic = damage_state_dic_generator(self.asset.hazus_class)
		self.k_skew = np.sqrt(np.sin((90-self.asset.skew_angle)*np.pi/180))
		self.k_3d = k3d_calculator(self.asset.hazus_class, self.asset.n_spans)

		self.mapped_conditions = []
		for key, val in self.damage_state_dic.items():
			self.mapped_conditions.append(val[-1])

		self.damage_state_dic['Slight'][MEDIAN] = self.damage_state_dic['Slight'][MEDIAN] * 1
		self.damage_state_dic['Moderate'][MEDIAN] = self.damage_state_dic['Moderate'][MEDIAN] * self.k_skew * self.k_3d
		self.damage_state_dic['Extensive'][MEDIAN] = self.damage_state_dic['Extensive'][MEDIAN] * self.k_skew * self.k_3d
		self.damage_state_dic['Collapse'][MEDIAN] = self.damage_state_dic['Collapse'][MEDIAN] * self.k_skew * self.k_3d

	def get(self, previous_condition = -1, soil_type = 'A', pga=None, pgd=0, sa_long=0.5, sa_short = 0.1):

		# Reference: HAZUS Manual
		sa_long = sa_long * long_period_modifier(sa_long, soil_type)

		probs = []
		previous_prob = 1
		if sa_long == 0:
			probs = [1, 0, 0, 0, 0]
		else:
			# Page 305 HAZUS
			for ds in self.damage_state_dic.keys():
				prob = norm.cdf(1/self.damage_state_dic[ds][BETA]*np.log(sa_long/self.damage_state_dic[ds][MEDIAN]))
				probs.append(previous_prob - prob)
				previous_prob = prob
			probs.append(prob)

		# Finding the mapped condition
		conds = [previous_condition] + self.mapped_conditions
		mapped_condition = np.random.choice(conds, p = probs)

		# Finding the corresponding damage state
		idx = conds.index(mapped_condition)
		ds = ['ds1', 'ds2', 'ds3', 'ds4', 'ds5'][idx]
			
		return max(mapped_condition, previous_condition), ds


def long_period_modifier(sa_long, soil_type):
	if soil_type == 'A':
		return 0.8
	elif soil_type == 'B':
		return 1.0
	elif soil_type == 'C':
		if sa_long < 0.1:
			return 1.7
		elif sa_long > 0.5:
			return 1.3
		else:
			return 1.8 - sa_long
	elif soil_type == 'D':
		if sa_long < 0.1:
			return 2.4
		elif sa_long > 0.5:
			return 1.5
		else:
			return 4.2557 * sa_long **2 - 4.7714 * sa_long + 2.82
		
	elif soil_type == 'E':
		if sa_long < 0.1:
			return 3.5
		elif sa_long > 0.5:
			return 2.4
		else:
			return 4.2857 * sa_long**2 - 5.5714 * sa_long + 4.06

def short_period_modifier(sa_short, soil_type):
	if soil_type == 'A':
		return 0.8
	elif soil_type == 'B':
		return 1.0
	elif soil_type == 'C':
		if sa_short < 0.25:
			return 1.2
		elif sa_short > 1.25:
			return 1.1
		else:
			return - 0.6 * sa_short + 1.28
	elif soil_type == 'D':
		if sa_short < 0.25:
			return 1.6
		elif sa_short > 1.25:
			return 1.0
		else:
			return 2.1429 * sa_short **2 - 2.7857 * sa_short + 1.86
		
	elif soil_type == 'E':
		if sa_short < 0.25:
			return 3.5
		elif sa_short > 1.25:
			return 2.4
		else:
			return 12.857 * sa_short**2 - 11.714 * sa_short + 3.54

def k3d_calculator(bridge_type, n_spans):
	if bridge_type in ['HWB1', 'HWB2', 'HWB3', 'HWB4', 'HWB5', 'HWB6', 'HWB7', 'HWB14', 'HWB17', 'HWB18', 'HWB19']:
		A, B = 0.25, 1
	elif bridge_type in ['HWB8', 'HWB10', 'HWB20', 'HWB22']:
		A, B = 0.33, 0
	elif bridge_type in ['HWB9', 'HWB11', 'HWB16', 'HWB21', 'HWB23']:
		A, B = 0.33, 1
	elif bridge_type in ['HWB12', 'HWB13']:
		A, B = 0.09, 1
	elif bridge_type in ['HWB15']:
		A, B = 0.05, 0
	elif bridge_type in ['HWB24', 'HWB25']:
		A, B = 0.2, 1
	elif bridge_type in ['HWB27']:
		A, B = 0.1, 0

	return 1 + A / max(n_spans - B, 1)

def i_shape_calculator(bridge_type):
	if bridge_type in ['HWB3', 'HWB4', 'HWB10', 'HWB11', 'HWB15', 'HWB16', 'HWB22', 'HWB23', 'HWB26', 'HWB27']:
		return 1
	return 0


def damage_state_dic_generator(bridge_type):
	medians = {'HWB1': [0.4, 0.5, 0.7, 0.9],
				'HWB2': [0.6, 0.9, 1.1, 1.7],
				'HWB3': [0.8, 1.0, 1.2, 1.7],
				'HWB4': [0.8, 1.0, 1.2, 1.7],
				'HWB5': [0.25, 0.35, 0.45, 0.70],
				'HWB6': [0.30, 0.50, 0.60, 0.90],
				'HWB7': [0.50, 0.80, 1.10, 1.70],
				'HWB8': [0.35, 0.45, 0.55, 0.80],
				'HWB9': [0.60, 0.90, 1.30, 1.60],
				'HWB10': [0.60, 0.90, 1.10, 1.50],
				'HWB11': [0.90, 0.90, 1.10, 1.50],
				'HWB12': [0.25, 0.35, 0.45, 0.70],
				'HWB13': [0.30, 0.50, 0.60, 0.90],
				'HWB14': [0.50, 0.80, 1.10, 1.70],
				'HWB15': [0.75, 0.75, 0.75, 1.10],
				'HWB16': [0.90, 0.90, 1.10, 1.50],
				'HWB17': [0.25, 0.35, 0.45, 0.70],
				'HWB18': [0.30, 0.50, 0.60, 0.90],
				'HWB19': [0.50, 0.80, 1.10, 1.70],
				'HWB20': [0.35, 0.45, 0.55, 0.80],
				'HWB21': [0.60, 0.90, 1.30, 1.60],
				'HWB22': [0.60, 0.90, 1.10, 1.50],
				'HWB23': [0.90, 0.90, 1.10, 1.50],
				'HWB24': [0.25, 0.35, 0.45, 0.70],
				'HWB25': [0.30, 0.50, 0.60, 0.90],
				'HWB26': [0.75, 0.75, 0.75, 1.10],
				'HWB27': [0.75, 0.75, 0.75, 1.10]
				}

	dispersion = 0.2

	damage_state_dic = {'Slight': [medians[bridge_type][0], dispersion, 2],
						'Moderate': [medians[bridge_type][1], dispersion, 3],
						'Extensive': [medians[bridge_type][2], dispersion, 5],
						'Collapse': [medians[bridge_type][3], dispersion, 5]}

	return damage_state_dic