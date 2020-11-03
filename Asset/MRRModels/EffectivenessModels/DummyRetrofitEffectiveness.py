import numpy as np

from .BaseMRREffectiveness import BaseMRREffectiveness

class DummyEffectiveness(BaseMRREffectiveness):
	
	def __init__(self):
		super().__init__()

		self.retrofit_effectiveness = np.array([[1     , 0     , 0   , 0   , 0   ],
											 	[0.8   , 0.2   , 0   , 0   , 0   ],
											 	[0.8   , 0.2   , 0   , 0   , 0   ],
											 	[0.8   , 0.2   , 0   , 0   , 0   ],
											 	[0.8   , 0.2   , 0   , 0   , 0   ]])


		self.effectiveness_dict = {self.BINAR: self.retrofit_effectiveness}

	def get(self, previous_state, action):
		
		rand = np.random.random()

		action_array = np.zeros(self.n_states)
		action_array[previous_state] = 1

		# Finding the probabilities of states corresponding to the action
		probability_array = np.dot(action_array, self.effectiveness_dict[action])

		# Finding the result of mrr
		for i, val in enumerate(probability_array):
			if rand < val:
				return i
			rand -= val