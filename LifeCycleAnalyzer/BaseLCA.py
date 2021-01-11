# Loading dependencies
import os
import logging
from utils.AwesomeLogger import Logger

class BaseLCA:

	def __init__(self, **params):
		super().__init__()

		'''The parent module of all future LCA modules

		::params::
		settings: the object that contain general settings
		network: the network for the analysis
		lca_name: the name for the analysis session
		simulator: the computational core that will be used in
			LCA analysis

		In contrast to other parent objects, methods are not 
			define here. The main reason is that the developers 
			could have the flesibility to extend the code to
			their needs with minimum limitations.
		'''
		self.lca_name = params.pop('lca_name', 'Unknown')
		self.settings = params.pop('settings')
		self.network = params.pop('network', None)
		self.simulator = params.pop('simulator', None)
		log_level = params.pop('log_level', logging.DEBUG)
		should_report = params.pop('should_report', False)

		if should_report:
			self.directory = f"reports/{self.lca_name}"
			if not os.path.exists(self.directory):
				os.mkdir(self.directory)

			dir = self.directory + "/Log.log"
			self.log = Logger (logger_name = 'Logger',
				                address = dir,
				                level = log_level,
				                console_level = logging.ERROR,
				                file_level = logging.DEBUG,
				                mode = 'a')

