import numpy as np

from .BaseMRREffectivenessModel import BaseMRREffectivenessModel

DONOT = 0
MAINT = 1
REHAB = 2
RECON = 3

class SimpleEffectiveness(BaseMRREffectivenessModel):
	
	def __init__(self):
		super().__init__()

		self.maintenance_effectiveness = np.array([[1   , 0   , 0   , 0   , 0   , 0   , 0   , 0   ],
											 	   [0.99, 0.01, 0   , 0   , 0   , 0   , 0   , 0   ],
											 	   [0.75, 0.24, 0.01, 0   , 0   , 0   , 0   , 0   ],
											 	   [0   , 0   , 0.20, 0.80, 0   , 0   , 0   , 0   ],
											 	   [0   , 0   , 0   , 0.10, 0.90, 0   , 0   , 0   ],
											 	   [0   , 0   , 0   , 0   , 0.01, 0.99, 0   , 0   ],
											 	   [0   , 0   , 0   , 0   , 0   , 0.01, 0.99, 0   ],
											 	   [0   , 0   , 0   , 0   , 0   , 0   , 0   , 1   ]])

		self.rehabilitation_effectiveness = np.array([[1   , 0   , 0   , 0   , 0   , 0   , 0   , 0   ],
											 	 	  [0.99, 0.01, 0   , 0   , 0   , 0   , 0   , 0   ],
											 	 	  [0.75, 0.24, 0.01, 0   , 0   , 0   , 0   , 0   ],
											 	 	  [0.45, 0.30, 0.24, 0.01, 0   , 0   , 0   , 0   ],
											 	 	  [0   , 0   , 0.75, 0.24, 0.01, 0   , 0   , 0   ],
											 	 	  [0   , 0   , 0   , 0.75, 0.24, 0.01, 0   , 0   ],
											 	 	  [0   , 0   , 0   , 0   , 0.75, 0.24, 0.01, 0   ],
											 	 	  [0   , 0   , 0   , 0   , 0   , 0.75, 0.24, 0.01]])

		self.reconstruction_effectiveness = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0],
											  		  [1, 0, 0, 0, 0, 0, 0, 0]])

		self.effectiveness_dict = {MAINT: self.maintenance_effectiveness, REHAB: self.rehabilitation_effectiveness, RECON: self.reconstruction_effectiveness}

	def get_effectiveness(self, previous_state, action):
		
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