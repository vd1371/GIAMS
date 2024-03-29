#Loading dependencies
import pandas as pd
import os
import sys

from utils.GeneralSettings import *

from Asset.AssetTypes.Bridge import Bridge
from Asset.AssetTypes.Building import Building

from Asset.Elements.BridgeElement import BridgeElement
from Asset.Elements.ConditionRating.NBIRatingModified import NBI
from Asset.Elements.Deterioration.IBMSSinha2009 import Markovian as MarkovianIBMS
from Asset.Elements.Utility.BridgeElementsUtilityBai2013 import *
from Asset.Elements.AgencyCost.AgencyCostSinha2009 import *

from Asset.Elements.BuildingElement import BuildingElement
from Asset.Elements.ConditionRating.PONTISRating import Pontis_CR
from Asset.Elements.Deterioration.Markovian import Markovian
from Asset.Elements.Utility.DummyBuildingUtility import DummyUtility
from Asset.Elements.AgencyCost.DummyBuildingRetrofitCost import RetrofitCosts

from Asset.Elements.SHMElement import SHMElement

from Asset.HazardModels.HazardModel import HazardModel
from Asset.HazardModels.Generator.PoissonProcess import PoissonProcess
from Asset.HazardModels.Response.HazusBridgeResponse import HazusBridgeResponse
from Asset.HazardModels.Loss.BridgeHazusLoss import BridgeHazusLoss
from Asset.HazardModels.Recovery.SimpleRecovery import SimpleRecovery

from Asset.HazardModels.Response.DummyBuildingResponse import DummyResponse
from Asset.HazardModels.Loss.DummyBuildingLoss import DummyLoss
from Asset.HazardModels.Recovery.DummyBuildingRecovery import DummyRecovery

from Asset.MRRModels.MRRFourActions import MRRFourActions
from Asset.MRRModels.MRRTwoActions import MRRTwoActions
from Asset.MRRModels.SHMActions import SHMActions
from Asset.MRRModels.EffectivenessModels.SimpleEffectiveness import SimpleEffectiveness
from Asset.MRRModels.EffectivenessModels.DummyRetrofitEffectiveness import DummyEffectiveness
from Asset.MRRModels.EffectivenessModels.SHMEffectiveness import SHMEffectiveness

from Asset.UserCostModels.TexasDOTUserCost import TexasDOTUserCost
from Asset.UserCostModels.TexasDOTUserCostWithVolatility import TexasDOTUserCostWithVolatility
from Asset.UserCostModels.DummyBuildingUserCost import DummyUserCost


from utils.AccumulatorThree import AccumulatorThree
from utils.AccumulatorX import AccumulatorX

from utils.PredictiveModels.Linear import Linear
from utils.PredictiveModels.WienerDrift import WienerDrift
from utils.PredictiveModels.GBM import GBM

from utils.Distributions.LogNormal import LogNormal
from utils.Distributions.Normal import Normal
from utils.Distributions.Beta import Beta
from utils.Distributions.Exponential import Exponential
from utils.Distributions.Gamma import Gamma
from utils.Distributions.Binomial import Binomial

class BaseNetwork:
	def __init__(self, **params):
		super().__init__()
		'''Constructor of the base network'''
		self.file_name = params.pop('file_name', None)
		self.n_assets = params.pop('n_assets', 0)
		self.settings = params.pop('settings')
		

		if not self.file_name is None:
			script_path = os.path.dirname(__file__)
			direc = os.path.join(script_path, f'Networks/{self.file_name}.csv')
			self.assets_df = pd.read_csv(direc, index_col = 0).iloc[:, :]
		
	def load_asset(self, *args, **kwargs):
		raise NotImplementedError ("load_asset in Loader is not implemented yet")

	def set_network_mrr(self, network_mrr):
		'''Setting the mrr of the network to each asset'''
		for asset, mrr in zip (self.assets, network_mrr):
			asset.mrr_model.set_mrr(mrr)
	
	def load_network(self):
		'''Loading the network
		
		If the file_name is None, it is assumed that the network will be randomized
		Else, the netwotk will be loaded from a datafile
		'''
		self.assets = []

		for idx in self.assets_df.index:
			# For loding data from file
			asset = self.load_asset(idx)
			if not asset == None:
				self.assets.append(asset)

			if len(self.assets) >= self.n_assets:
				break

		return self.assets

	def set_current_budget_limit(self, val):
		'''Setting the current budget limit'''
		self.current_budget_limit = val

	def set_budget_limit_model(self, model):
		self.budget_limit_model = model

	def set_annual_budget_limit_model(self, model):
		'''Setting the budget limit in time'''
		self.annual_budget_model = model
		
	def set_npv_budget_limit(self, val):
		'''Set the npv of the budget limit'''
		self.npv_budget_limit = val

	def objective1(self):
		return np.random.random()

	def objective2(self):
		return np.random.random()
	
	