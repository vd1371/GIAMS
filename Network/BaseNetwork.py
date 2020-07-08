import pandas as pd
import sys

from utils.GeneralSettings import GenSet

from Asset.AssetTypes.Bridge import Bridge

from Asset.Elements.BridgeElement import BridgeElement
from Asset.Elements.ConditionRating.NBIRatingModified import NBI
from Asset.Elements.Deterioration.MarkovianSinha2009 import Markovian
from Asset.Elements.Utility.BridgeElementsUtilityBai2013 import *
from Asset.Elements.AgencyCost.AgencyCostSinha2009 import * 

from Asset.HazardModels.Generator.PoissonProcess import PoissonProcess
from Asset.HazardModels.Response.HazusBridgeResponse import HazusBridgeResponse
from Asset.HazardModels.Loss.HazusLossModel import HazusLossModel
from Asset.HazardModels.Recovery.SimpleRecoveryModel import SimpleRecoveryModel

from Asset.MRRModels.MRRFourActions import MRRFourActions
from Asset.MRRModels.EffectivenessModels.SimpleEffectiveness import SimpleEffectiveness

from Asset.UserCostModels.TexasDOTUserCost import TexasDOTUserCost

from utils.Accum import Accum

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
    def __init__(self, file_name = None):
        super().__init__()
        
        self.file_name = file_name
        dir = f'./Network/Networks/{file_name}.csv'
        self.assets_df = pd.read_csv(dir, index_col = 0)
        
    def load_asset(self):
        raise NotImplementedError ("load_asset in Loader is not implemented yet")
    
    def load_network(self):
        raise NotImplementedError ("load_network in loader is not implemented yet")
    
    def set_current_budget_limit(self, val):
        self.current_budget_limit = val

    def set_budget_limit_model(self, model):
        self.budget_model = model
        
    def set_npv_budget_limit(self, val):
        self.npv_budget_limit = val

    def set_network_mrr(self, network_mrr):
        for asset, mrr in zip (self.assets, network_mrr):
            asset.mrr_model.set_mrr(mrr)

def predictive_model(p_type, X0, first_param, second_param):
    
    if p_type == 'Linear':
        return Linear(X0 = X0, drift = first_param)
    elif p_type == 'WienerDrift':
        return WienerDrift(X0 = X0, drift = first_param, volatility = second_param)
    elif p_type == 'GBM':
        return GBM(X0 = X0, drift = first_param, volatility = second_param)
    else:
        raise ValueError (f"({p_type}) predictive model is not implemented yet in the loader")

def distribution(d_type, first_param, second_param):
    if d_type == 'LogNormal':
        return LogNormal(first_param, second_param)
    elif d_type == 'Normal':
        return Normal(first_param, second_param)
    elif d_type == 'Exponential':
        return Exponential(first_param)
    elif d_type == 'Binomial':
        return Binomial(first_param, second_param)
    elif d_type == 'Gamma':
        return Gamma(first_param, second_param)
    elif d_type == 'Binomial':
        return Binomial(first_param, second_param)

    else:
        raise ValueError (f"{d_type} distribution model is not implemented yet in the loader")
        
    
    