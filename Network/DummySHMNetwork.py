import numpy as np

from .BaseNetwork import *

class IndianaNetwork(BaseNetwork):
    
    def __init__(self, **params):
        super().__init__(**params)
        self.is_deck = params.pop('is_deck')
        self.is_substructure = params.pop('is_substructure')
        self.is_superstructure = params.pop('is_superstructure')
        
    def load_asset(self, idx = 0):
        
        asset_info = self.assets_df.loc[idx, :]
        
        id_, length, width, material, design = asset_info[0:5]
        vertical_clearance = asset_info[21]
        asset = Bridge(ID = id_,
                        length = length,
                        width = width,
                        material = material,
                        design = design,
                        vertical_clearance = vertical_clearance,
                        settings = self.settings)

        asset.set_accumulator(AccumulatorX)

        # Setting traffic info
        road_class, ADT, truck_percentage, detour_length = asset_info[5:9]
        asset.set_traffic_info(road_class = road_class,
                                ADT = ADT,
                                truck_percentage = truck_percentage,
                                detour_length = detour_length)
        
        # Setting seismic info
        hazus_class, site_class, skew_angle, n_spans = asset_info[9:13]
        asset.set_seismic_info(hazus_class = hazus_class,
                                site_class = site_class,
                                skew_angle = skew_angle,
                                n_spans = n_spans)
        
        # Setting MRR durations and effectiveness models
        maint_duration, rehab_duration, recon_duration = asset_info[13:16]
        mrr = SHMActions(settings = self.settings)
        
        mrr.set_effectiveness(SimpleEffectiveness(settings = self.settings))
        asset.set_mrr_model(mrr)

        # User cost model
        asset.set_user_cost_model(DummyUserCost(settings = self.settings))
        
        # Hazard models
        hazard_model = HazardModel()
        hazard_model.set_asset(asset)
        "Only earthquakes with magnitude of 4 or higher and based on historical data from USGS"
        hazard_model.set_generator_model(PoissonProcess(occurrence_rate = 0.3, dist = Exponential(2.1739, 4))) 
        hazard_model.set_response_model(HazusBridgeResponse(asset))
        hazard_model.set_loss_model(BridgeHazusLoss(settings = self.settings))
        hazard_model.set_recovery_model(SimpleRecovery(settings = self.settings))
        asset.set_hazard_model(hazard_model)
        asset.set_replacement_value_model(hazus_default = True)
        
        # Finding the age
        age = asset_info [16]

        if self.is_superstructure:
            # Adding the superstructure to the asset
            superstructure_cond = asset_info [19]
            superstructure = BridgeElement(name = SUPERSTRUCTURE,
                                            initial_condition = min(9-superstructure_cond, 7),
                                            age = age,
                                            settings = self.settings)
            superstructure.set_asset(asset)
            superstructure.set_condition_rating_model(NBI())
            superstructure.set_deterioration_model(MarkovianIBMS())
            superstructure.set_utility_model(SuperstructureUtility())
            superstructure.set_agency_costs_model(SuperstructureCosts(settings = self.settings))
            asset.add_element(superstructure)
 
        return asset
