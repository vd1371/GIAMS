#Loading dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .GeneralSettings import *
from .NPV import NPV
from .Container import Container

class AccumulatorX:
	def __init__(self, **params):
		'''Accumulator object

		This class stores the simulation results,
			draw figures based on them, and possibly store the contents
		Parameters to be monitored should be passed through to_store

		::params::
		settings: analysis settings
		ID: asset ID
		to_store: parameters to be stored
		'''
		self.settings = params.pop("settings")
		self.ID = params.pop("ID")
		self.to_store = params.pop("to_store")

		self.refresh()
		
	def refresh(self):
		self.meta_data = {k: Container(settings = self.settings) for k in self.to_store}

	def update(self, **analysis_results):

		for key, values in analysis_results.items():

			self.meta_data[key].add_to_npv_samples(values)
			self.meta_data[key].update_stepwise(values)

	def log_results(self, logger, directory):

		df = pd.DataFrame()
		for key, container_ in self.meta_data.items():
			logger.info(f"Asset {self.ID} "\
							f"costs: Mean, Stdv:{container_.expected()}")

			df[key] = container_.get_samples()

		df.to_csv(directory + f"/Asset{self.ID}-SimulationResults.csv")

		plt.clf()
		df.hist(density = False,  figsize=(20, 10))
		plt.savefig(directory + f"/Asset{self.ID}-Histogram.png")

	def __repr__(self):
		return "Not yet implemented"
	
	def __str__(self):
		return "Not yet implemented"





