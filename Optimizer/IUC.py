import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from itertools import permutations, product
import pprint


from utils.GeneralSettings import GenSet

'''
This IUC optimiztion is built on the premise that we have 4 different types of actions
Do nothing, maintenance, rehabiliation, reconstruction
'''

def to_binary(actions):
	elements_mrr = []
	for val in actions:
		if val == 0:
			elements_mrr += [[0, 0]]
		elif val == 1:
			elements_mrr += [[0, 1]]
		elif val == 2:
			elements_mrr += [[1, 0]]
		elif val == 3:
			elements_mrr += [[1, 1]]

class IUC(GenSet):
	def __init__(self, lca = None):

		# Gettign the objective function
		self.lca = lca()

		n_assets = len(self.lca.network.assets)
		self.asset_mrr_shape = self.lca.network.assets[0].mrr_model.mrr.shape
		self.network_mrr_shape = (n_assets, self.asset_mrr_shape[0], self.asset_mrr_shape[1])

		self.possible_mrrs = list(product([0,1], repeat=self.n_elements * 2))

	def optimize(self):

		network_mrr = np.zeros(self.network_mrr_shape)

		for step in range(self.n_steps):

			start = time.time()
			assessment_dic = {}
			for asset_idx, asset in enumerate(self.lca.network.assets):

				print (f"Asset {asset_idx + 1} is about to be processed at step {step+1} / {self.n_steps}")

				mrr = np.copy(network_mrr[asset_idx])

				for possible_mrr_idx, possible_mrr in enumerate(self.possible_mrrs):

					# Assigning a possible mrr plan
					for elem_idx, element in enumerate(asset.elements):
						mrr[elem_idx][step*self.dt] = possible_mrr[elem_idx*self.dt]
						mrr[elem_idx][step*self.dt + 1] = possible_mrr[elem_idx*self.dt + 1]

					# Assigning it to the
					asset.mrr_model.set_mrr(mrr)

					# Running the simulation
					self.lca.run_for_one_asset(asset)

					# Let's get the costs
					user_costs = asset.accumulator.user_costs.at_year(step*self.dt)
					agency_costs = asset.accumulator.agency_costs.at_year(step*self.dt)
					asset_utils = asset.accumulator.asset_utils.at_year(step*self.dt)

					# Find the utiliti/cost and agency costs
					U_C = asset_utils/(user_costs + agency_costs) if agency_costs != 0 else 0

					# Adding the results to the assessment dic
					hash_key = hash(str(asset.ID) + str(step) + str(possible_mrr)) 
					assessment_dic[hash_key] = [asset.ID, asset_idx, U_C, agency_costs, np.copy(possible_mrr), user_costs]

			# Sorting the actions based on U/C
			# item [1][1] refers to the values of the dictionary and U_C
			assessment_dic = {k: v for k, v in sorted(assessment_dic.items(), key=lambda item: item[1][2], reverse = True)}

			# Finding the budget at the step
			remaining_budget = self.lca.network.budget_model.predict_series(random = False)[step]
			planned_assets = []

			# Update the network_mrr based on the budget and the assessment dic
			temp_dic = {}
			for k, v in assessment_dic.items():

				asset_id, asset_idx, U_C, agency_costs, temp_mrr, user_costs = v

				# If the asset is not in the planned_assets
				# and if its agency costs is less than the remaining budget (to meet the budget limitations)
				# and if the U_C > 0 (To prevent working on an intanct object)
				if not asset_id in planned_assets and agency_costs < remaining_budget and U_C > 0:

					# Add the asset to the planned_assets holder
					planned_assets.append(asset_id)
					
					# Deduct the cost from the remaining budget
					remaining_budget -= agency_costs

					# Set the corresponding mrr to the network mrr
					for elem_idx, element in enumerate(asset.elements):
						network_mrr[asset_idx][elem_idx][step*self.dt] = temp_mrr[elem_idx*self.dt]
						network_mrr[asset_idx][elem_idx][step*self.dt + 1] = temp_mrr[elem_idx*self.dt + 1]

					temp_dic[asset_id] = list(network_mrr[asset_idx].reshape(1, -1)[0]) + [U_C, agency_costs, user_costs]

			print (f"Step {step} is analyzed and optimized in {time.time() - start:.2f} seconds")

		# Turning temp_dic to a dataframe
		cols = []
		for i in range (self.n_elements):
			for j in range (2):
				cols.append(f'Elem{i}-{j}')
		cols += ['U_C', 'AgencyCosts', 'UserCosts']
		df = pd.DataFrame.from_dict(temp_dic, orient='index', columns = cols)
		df.index.rename('ID')
		df.iloc[:, :6] = df.iloc[:, :6].astype(int)
		df.to_csv(self.lca.directory + f"/{self.lca.lca_name}.csv")

		print ("IUC optimization is done")









				







