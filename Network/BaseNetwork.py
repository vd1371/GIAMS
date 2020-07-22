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
from Asset.HazardModels.Loss.HazusLossModel import HazusLossModel
from Asset.HazardModels.Recovery.SimpleRecoveryModel import SimpleRecoveryModel

from Asset.MRRModels.MRRFourActions import MRRFourActions
from Asset.MRRModels.EffectivenessModels.SimpleEffectiveness import SimpleEffectiveness

from Asset.UserCostModels.TexasDOTUserCost import TexasDOTUserCost

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
        
        dir = f'./Network/Networks/{file_name}.csv'
        self.assets_df = pd.read_csv(dir, index_col = 0).iloc[:self.n_assets, :]
        
    def load_asset(self, *args, **kwargs):
        raise NotImplementedError ("load_asset in Loader is not implemented yet")
    
    def load_network(self, *args, **kwargs):
        raise NotImplementedError ("load_network in loader is not implemented yet")

    def set_network_mrr(self, network_mrr):
        for asset, mrr in zip (self.assets, network_mrr):
            asset.mrr_model.set_mrr(mrr)
        
    
    