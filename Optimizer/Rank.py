import time
import numpy as np
import pprint
from collections import OrderedDict

class Rank:
	def __init__(self, **params):
		'''Rank optimization'''
		# Gettign the objective function
		self.lca = params.pop('lca')
		self.settings = params.pop('settings')

	def optimize(self):

		assessment_dic = {}
		for asset in self.lca.network.assets:

			# Ruinning the simulation
			self.lca.run_for_one_asset(asset)

			# Let's get the risk
			val, _ = asset.accumulator.asset_utils.expected()

			# Adding to the dictionary
			assessment_dic[asset] = val

		assessment_dic = dict(sorted(assessment_dic.items(), key=lambda item: item[1]))
		
		print ("Rank optimization is done")
		return assessment_dic









				







