import time


from Network.IndianaNetwork import IndianaNetwork
from LifeCycleAnalyzer.Simulators.MainSimulator import MainSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


if __name__ == "__main__":

	# GA_test(lca)
	# IUC_test(lca)
	# my_lca = lca()


	from Examples.Example1 import example1
	example1()
	# from Examples.Example3 import example
	# from Examples.Example3 import validate_ga

	
	# from Examples.BuildingRetrofitDummy import example
	# example()

