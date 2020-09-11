import numpy as np

from .BaseNetwork import *

class RandomNetwork(BaseNetwork):
    
    def __init__(self, file_name, n_assets):
        super().__init__(file_name, n_assets)
        
    def load_asset(self):

        prm = {'id' : hash(str(np.random.random()*np.random.random())), 
                    'length' : np.random.random_integers(5, 1800),
                    'width' : np.random.random_integers(3, 60),
                    'material': np.random.choice([1, 2, 3, 4, 5, 6]),
                    'design': np.random.choice([1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 16, 21, 22]),
                    'vertical_clearance': np.random.uniform(4, 7),
                    'road_class': np.random.choice(['Local', 'Major', 'Minor', 'NHS']),
                    'ADT': np.random.random_integers(100, 400000),
                    'truck_percentage': np.random.uniform(0, 0.99),
                    'detour_length': np.random.random_integers(1, 200),
                    'hazus_class': 'HWB' + str(np.random.choice([1, 3, 5, 8, 10, 12, 15, 17, 22])),
                    'site_class': np.random.choice(['A', 'B', 'C']),
                    'skew_angle': np.random.random_integers(0, 45),
                    'n_spans': int(np.random.random_integers(1, 60)),
                    'maint_duration': np.random.random_integers(10, 60),
                    'rehab_duration': np.random.random_integers(120, 240),
                    'recon_duration': np.random.random_integers(300, 540),
                    'speed_before': np.random.random_integers(40, 90),
                    'speed_after': np.random.random_integers(15, 35),
                    'drift': np.random.uniform(0.01, 0.1),
                    'volatility': np.random.uniform(0.01, 0.1),
                    'detour_usage_percentage': np.random.uniform(0, 0.99),
                    'occurrence_rate': np.random.uniform(0.001, 0.1),
                    'dist_first_param': np.random.uniform(3, 5),
                    'dist_second_param': np.random.uniform(0.01, 2),
                    'deck_cond': np.random.choice([9, 8, 7, 6, 5, 4]),
                    'deck_age': np.random.random_integers(1, 90),
                    'deck_material': np.random.choice([1, 2, 3, 8]),
                    'superstructure_cond': np.random.choice([9, 8, 7, 6, 5, 4]),
                    'superstructure_age': np.random.random_integers(1, 90),
                    'substructure_cond': np.random.choice([9, 8, 7, 6, 5, 4]),
                    'substructure_age': np.random.random_integers(1, 90)
                    }
        
        id_, length, width, \
            material, design, vertical_clearance = prm['id'], prm['length'], prm['width'], \
                                                                            prm['material'], prm['design'], prm['vertical_clearance']
        asset = Bridge(ID = id_, length = length,
                                width = width,
                                material = material,
                                design = design,
                                vertical_clearance = vertical_clearance)
        asset.set_accumulator(Accumulator)

        # Setting traffic info
        road_class, ADT, truck_percentage, detour_length = prm['road_class'], prm['ADT'], prm['truck_percentage'], prm['detour_usage_percentage']
        asset.set_traffic_info(road_class = road_class, ADT = ADT, truck_percentage = truck_percentage, detour_length = detour_length)
        
        # Setting seismic info
        hazus_class, site_class, skew_angle, n_spans = prm['hazus_class'], prm['site_class'], prm['skew_angle'], prm['n_spans']
        asset.set_seismic_info(hazus_class = hazus_class, site_class = site_class, skew_angle = skew_angle, n_spans = n_spans)
        
        # Setting MRR durations and effectiveness models
        maint_duration, rehab_duration, recon_duration = prm['maint_duration'], prm['rehab_duration'], prm['recon_duration']
        mrr = MRRFourActions(maint_duration = maint_duration, rehab_duration = rehab_duration, recon_duration = recon_duration)
        mrr.set_effectiveness(SimpleEffectiveness())
        asset.set_mrr_model(mrr)

        # Randomizing the mrr model
        p = np.random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
        random_mrr = np.random.choice([0, 1], size = [self.n_elements, self.n_steps*self.dt], p = [1-p, p])
        asset.mrr_model.set_mrr(random_mrr)


        # User cost model
        speed_before, speed_after, drift,\
             volatility, detour_usage_percentage = prm['speed_before'], prm['speed_after'],\
                                                        prm['drift'], prm['volatility'], prm['detour_usage_percentage']
        asset.set_user_cost_model(TexasDOTUserCostWithVolatility(speed_before = speed_after,
                                                                speed_after = speed_after,
                                                                drift = drift,
                                                                volatility = volatility,
                                                                detour_usage_percentage = detour_usage_percentage))
        
        # Hazard models
        hazard_model = HazardModel()
        hazard_model.set_asset(asset)
        "Only earthquakes with magnitude of 4 or higher and based on historical data from USGS"
        occurrence_rate, dist_first_param, dist_second_param = prm['occurrence_rate'], prm['dist_first_param'], prm['dist_second_param']
        hazard_model.set_generator_model(PoissonProcess(occurrence_rate = occurrence_rate,
                                                        dist = LogNormal(dist_first_param, dist_second_param))) 
        hazard_model.set_response_model(HazusBridgeResponse(asset))
        hazard_model.set_loss_model(HazusLoss())
        hazard_model.set_recovery_model(SimpleRecovery())
        asset.set_hazard_model(hazard_model)
        asset.set_replacement_value_model(hazus_default = True)

        # Adding the deck to the asset
        deck_age, deck_material, deck_cond = prm['deck_age'], prm['deck_material'], prm['deck_cond']
        deck = BridgeElement(name = DECK,
                            initial_condition = min(9-deck_cond, 7),
                            age = deck_age,
                            material = deck_material)
        deck.set_asset(asset)
        deck.set_condition_rating_model(NBI())
        deck.set_deterioration_model(Markovian())
        deck.set_utility_model(DeckUtility())
        deck.set_agency_costs_model(DeckCosts())
        asset.add_element(deck)

        # Adding the superstructure to the asset
        superstructure_age, superstructure_cond = prm['superstructure_age'], prm['superstructure_cond']
        superstructure = BridgeElement(name = SUPERSTRUCTURE,
                                        initial_condition = min(9-superstructure_cond, 7),
                                        age = superstructure_age)
        superstructure.set_asset(asset)
        superstructure.set_condition_rating_model(NBI())
        superstructure.set_deterioration_model(Markovian())
        superstructure.set_utility_model(SuperstructureUtility())
        superstructure.set_agency_costs_model(SuperstructureCosts())
        asset.add_element(superstructure)

        # Adding the substruture to the asset
        substructure_age, substructure_cond = prm['substructure_age'], prm['substructure_cond']
        substructure = BridgeElement(name = SUBSTRUCTURE,
                                    initial_condition = min(9-substructure_cond,7),
                                    age = substructure_age)
        substructure.set_asset(asset)
        substructure.set_condition_rating_model(NBI())
        substructure.set_deterioration_model(Markovian())
        substructure.set_utility_model(SubstructureUtility())
        substructure.set_agency_costs_model(SubstructureCosts())
        asset.add_element(substructure)
 
        return asset, prm
    
    def load_network(self):
        
        assets = []

        asset, params = self.load_asset()
        assets.append(asset) 
        
        self.assets = assets
        return params

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
