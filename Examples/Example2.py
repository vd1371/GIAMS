# -------------------------------------------------------------------- #
# This example was designed to show the IUC optimization option in GIAMS
# This example was used in the original paper as well
# -------------------------------------------------------------------- #



import time


from Network.IndianaNetwork import IndianaNetwork
from LifeCycleAnalyzer.Simulators.MainSimulator import MainSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


class GeneralSettings:

	n_elements = 3
	n_states = 8
	dt = 2
	horizon = 20
	discount_rate = 0.03
	init_year = 0
	n_steps = int(horizon/dt)

settings = GeneralSettings()

def lca():

	session_name = 'Indiana-IUC'
	mynetwork = IndianaNetwork(file_name = "INDIANA2019",
								n_assets = -1,
								settings = settings,
								is_deck = True,
				                is_superstructure = True,
				                is_substructure = True)
	mynetwork.load_network()

	mynetwork.set_current_budget_limit(10000)
	mynetwork.set_budget_limit_model(Linear(X0 = 10000, drift = 0, settings = settings))
	mynetwork.set_npv_budget_limit(100000)

	simulator = MainSimulator(settings = settings)
	lca = LCA(lca_name = session_name,
			settings = settings,
			network = mynetwork,
			simulator = simulator,
			random = False,
			is_hazard = False,
			n_simulations = 5,
			should_report = True)

	return lca

@timeit
def IUC_test():

	optimizer = IUC(lca = lca, settings = settings)
	optimizer.optimize()


if __name__ == "__main__":
	
	IUC_test(lca)

