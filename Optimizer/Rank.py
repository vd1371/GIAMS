import time
import numpy as np
import pprint
from collections import OrderedDict

from utils.GeneralSettings import GenSet

'''
This rank module
'''


class Rank(GenSet):
	def __init__(self, lca = None):

		# Gettign the objective function
		self.lca = lca()

	def optimize(self):

		assessment_dic = {}

		for asset in self.lca.network.assets:

			# Ruinning the simulation
			self.lca.run_for_one_asset(asset)

			# Let's get the risk
			risk, _ = asset.accumulator.asset_utils.expected()

			# Adding to the dictionary
			assessment_dic[asset] = risk

		assessment_dic = dict(sorted(assessment_dic.items(), key=lambda item: item[1]))
		
		print ("Rank optimization is done")
		return assessment_dic









				







