import os, sys
import logging
import time
import numpy as np
import matplotlib.pyplot as plt

from utils.AwesomeLogger import Logger
from utils.GeneralSettings import GenSet

class BaseLCA(GenSet):

	def __init__(self, network = None,
						lca_name = 'Unknown',
						simulator = None,
						log_level = logging.DEBUG,
						should_report = True):
		super().__init__()

		self.network = network
		self.lca_name = lca_name
		self.simulator = simulator


		if should_report:
			self.directory = f"reports/{lca_name}"
			if not os.path.exists(self.directory):
				os.mkdir(self.directory)

			dir = self.directory + "/Log.log"
			self.log = Logger (logger_name = 'Logger',
				                address = dir,
				                level = log_level,
				                console_level = logging.ERROR,
				                file_level = logging.DEBUG,
				                mode = 'a')

