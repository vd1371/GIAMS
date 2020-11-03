import pandas as pd
import sys

from utils.GeneralSettings import *

from Asset.AssetTypes.Bridge import Bridge

from Asset.Elements.BridgeElement import BridgeElement
from Asset.Elements.ConditionRating.NBIRatingModified import NBI
from Asset.Elements.Deterioration.IBMSSinha2009 import Markovian
from Asset.Elements.Utility.BridgeElementsUtilityBai2013 import *
from Asset.Elements.AgencyCost.AgencyCostSinha2009 import * 

from Asset.HazardModels.HazardModel import HazardModel
from Asset.HazardModels.Generator.PoissonProcess import PoissonProcess
from Asset.HazardModels.Response.HazusBridgeResponse import HazusBridgeResponse
from Asset.HazardModels.Loss.BridgeHazusLoss import BridgeHazusLoss
from Asset.HazardModels.Recovery.SimpleRecovery import SimpleRecovery

from Asset.MRRModels.MRRFourActions import MRRFourActions
from Asset.MRRModels.EffectivenessModels.SimpleEffectiveness import SimpleEffectiveness

from Asset.UserCostModels.TexasDOTUserCost import TexasDOTUserCost
from Asset.UserCostModels.TexasDOTUserCostWithVolatility import TexasDOTUserCostWithVolatility

from utils.Accumulator import Accumulator

from utils.PredictiveModels.Linear import Linear
from utils.PredictiveModels.WienerDrift import WienerDrift
from utils.PredictiveModels.GBM import GBM

from utils.Distributions.LogNormal import LogNormal
from utils.Distributions.Normal import Normal
from utils.Distributions.Beta import Beta
from utils.Distributions.Exponential import Exponential
from utils.Distributions.Gamma import Gamma
from utils.Distributions.Binomial import Binomial

class BaseNetwork(GenSet):
    def __init__(self, file_name = None, n_assets = 0):
        super().__init__()
        
        self.file_name = file_name
        self.n_assets = n_assets
        
        if not file_name is None:
            dir = f'./Network/Networks/{file_name}.csv'
            self.assets_df = pd.read_csv(dir, index_col = 0).iloc[:self.n_assets, :]
        
    def load_asset(self, *args, **kwargs):
        raise NotImplementedError ("load_asset in Loader is not implemented yet")
    
    def load_network(self, *args, **kwargs):
        raise NotImplementedError ("load_network in loader is not implemented yet")

    def set_network_mrr(self, network_mrr):
        for asset, mrr in zip (self.assets, network_mrr):
            asset.mrr_model.set_mrr(mrr)
    
    def load_network(self):
        
        self.assets = []
        if self.file_name is None:
            # For generated networks
            for i in range (self.n_assets):
                self.assets.append(self.load_asset())
        else:
            for idx in self.assets_df.index:
                # For loding data from file
                self.assets.append(self.load_asset(idx))

        return self.assets

    def set_current_budget_limit(self, val):
        self.current_budget_limit = val

    def set_budget_limit_model(self, model):
        self.budget_model = model
        
    def set_npv_budget_limit(self, val):
        self.npv_budget_limit = val

    def objective1(self):
        return np.random.random()

    def objective2(self):
        return np.random.random()
    
    