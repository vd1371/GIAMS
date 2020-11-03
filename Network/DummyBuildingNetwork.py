import numpy as np

from .BaseNetwork import *

from Asset.AssetTypes.Building import Building

from Asset.Elements.BuildingElement import BuildingElement
from Asset.Elements.ConditionRating.PONTISRating import Pontis_CR
from Asset.Elements.Deterioration.Markovian import Markovian
from Asset.Elements.Utility.DummyBuildingUtility import DummyUtility
from Asset.Elements.AgencyCost.DummyBuildingRetrofitCost import RetrofitCosts

from Asset.HazardModels.HazardModel import HazardModel
from Asset.HazardModels.Generator.PoissonProcess import PoissonProcess
from Asset.HazardModels.Response.DummyBuildingResponse import DummyResponse
from Asset.HazardModels.Loss.DummyBuildingLoss import DummyLoss
from Asset.HazardModels.Recovery.DummyBuildingRecovery import DummyRecovery

from Asset.MRRModels.MRRTwoActions import MRRTwoActions
from Asset.MRRModels.EffectivenessModels.DummyRetrofitEffectiveness import DummyEffectiveness

from Asset.UserCostModels.DummyBuildingUserCost import DummyUserCost

from utils.Accumulator import Accumulator

from utils.PredictiveModels.Linear import Linear
from utils.Distributions.Normal import Normal

class BuildingNetwork(BaseNetwork):
    
    def __init__(self, file_name, n_assets):
        super().__init__(file_name, n_assets)
        
    def load_asset(self):

        prm = {'id' : hash(str(np.random.random()*np.random.random())), 
                    'height' : np.random.random_integers(5, 20),
                    'width' : np.random.random_integers(3, 60),
                    'structural_type': np.random.choice(['Steel', 'Concrete']),
                    'site_class': np.random.choice(['A', 'B', 'C']),
                    'age': np.random.random_integers(1, 90)
                    }
        
        id_, height, width, \
            structural_type, site_class, age = prm['id'], prm['height'], prm['width'], \
                                            prm['structural_type'], prm['site_class'], prm['age']
        asset = Building(ID = id_, height = height,
                                width = width)
        asset.set_accumulator(Accumulator)

        asset.set_seismic_info(structural_type = structural_type, site_class = site_class)
        
        # Setting MRR durations and effectiveness models
        mrr = MRRTwoActions(action_duration = 60)
        mrr.set_effectiveness(DummyEffectiveness())
        asset.set_mrr_model(mrr)

        # User cost model
        asset.set_user_cost_model(DummyUserCost())
        
        # Hazard models
        hazard_model = HazardModel()
        hazard_model.set_asset(asset)
        "Only earthquakes with magnitude of 4 or higher and based on historical data from USGS"
        hazard_model.set_generator_model(PoissonProcess(occurrence_rate = 0.01,
                                                        dist = LogNormal(3, 2))) 
        hazard_model.set_response_model(DummyResponse(asset))
        hazard_model.set_loss_model(DummyLoss())
        hazard_model.set_recovery_model(DummyRecovery())
        asset.set_hazard_model(hazard_model)
        asset.set_replacement_value_model(hazus_default = True)

        # Adding the structure to the asset
        structure = BuildingElement(name = 'Structure',
                            initial_condition = np.random.choice([0, 1, 2, 3]),
                            age = age)
        structure.set_asset(asset)
        structure.set_condition_rating_model(Pontis_CR())
        structure.set_deterioration_model(Markovian([0.95, 0.9, 0.85, 0.8, 1]))
        structure.set_utility_model(DummyUtility())
        structure.set_agency_costs_model(RetrofitCosts())
        asset.add_element(structure)
 
        return asset
