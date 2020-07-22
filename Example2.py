import time


from Network.IndianaNetwork import IndianaNetwork
from LifeCycleAnalyzer.Simulators.BridgeSimulator import BridgeSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


def lca():

	session_name = 'Indiana-IUC'
	
	mynetwork = IndianaNetwork("INDIANA2019", n_assets = -1)
	mynetwork.load_network()

	# mynetwork.assets[0].mrr_model.set_mrr(np.array([[1,1,1,1,1,0,0,0,1,0,1,0], [1,0,1,0,1,0,1,0,1,0,1,1], [0,0,0,0,1,1,0,0,0,1,1,1]]))
	mynetwork.set_current_budget_limit(10000)
	mynetwork.set_budget_limit_model(Linear(X0 = 10000, drift = 0))
	mynetwork.set_npv_budget_limit(100000)

	simulator = BridgeSimulator()
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = False,
			is_hazard = False)

	return lca

@timeit
def IUC_test(obj):

	optimizer = IUC(obj)
	optimizer.optimize()


if __name__ == "__main__":
	
	IUC_test(lca)

