import numpy as np
from .BaseResponseModel import BaseResponseModel


class BridgeEarthQuakeResponse(BaseResponseModel):

	def __init__(self, damage_state_dic = {'Slight': [0.5*1, 0.6, 2],
											'Moderate': [0.8*1*1.125, 0.6, 3],
											'Extensive': [1.1*1*1.125, 0.6, 5],
											'Complete': [1.7*1*1.125, 0.6, 5]}):
		super().__init__()
		self.damage_state_dic = damage_state_dic

	def get_response(self, previous_condition = -1, pga=None, pgd=0, sa_long=0, sa_short = 0):

		#TODO: Make the output states more clear and rational
		#TODO: Make the connection between the condition rates and damage states

		MEDIAN = 0 # It's just an index, to make it more clear to read
		BETA = 1 # It's just an index, to make it more clear to read

		states = [previous_condition]
		for key, val in self.damage_state_dic.items():
			states.append(val[-1])

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
			
		return np.random.choice(states, p = probs)