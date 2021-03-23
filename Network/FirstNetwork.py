import numpy as np

from .BaseNetwork import *

class FirstNetwork(BaseNetwork):
    
    def __init__(self, file_name):
        super().__init__(file_name)
        
    def load_asset(self, idx = 0):
        '''Loading asset for the first time analysis and testing GIAMS
        
        This example is out of date.
        '''
        
        asset_info = self.assets_df.iloc[idx, :]
        
        id = asset_info[0]
        asset = Bridge(ID = id)
        asset.set_accumulator(Accum)
        
        bridge_type, soil_type, skew_angle, n_spans = asset_info[1:5]
        asset.set_seismic_chars(bridge_type = bridge_type,
                                    soil_type = soil_type,
                                    skew_angle = skew_angle,
                                    n_spans = n_spans)
        
        # MRR Chars
        maint_duration, rehab_duration, recon_duration = asset_info [5:8]
        asset.set_mrr_model(MRRFourActions( maint_duration = maint_duration,
                                            rehab_duration = rehab_duration,
                                            recon_duration = recon_duration))
        
        asset.set_mrr_effectiveness_model(SimpleEffectiveness())

        # User cost model
        ADT, percent_truck, speed_before, speed_after, segment_length, detour_length, detour_usage_percentage = asset_info[8:15]
        asset.set_user_cost_model(TexasDOTUserCost(ADT = ADT,
                                                    percent_truck = percent_truck,
                                                    speed_before = speed_before,
                                                    speed_after = speed_after,
                                                    segment_length = segment_length,
                                                    detour_length = detour_length,
                                                    detour_usage_percentage = detour_usage_percentage))
        
        # Hazard related info
        eq_rate, d_type, eq_dist_first_param, eq_dist_second_param = asset_info[15:19]
        eq_model = PoissonProcess(occurrence_rate = eq_rate)
        eq_model.set_magnitude_distribution(distribution(d_type, eq_dist_first_param, eq_dist_second_param))
        asset.set_hazard_model(eq_model)
        asset.set_hazard_response_model(HazusBridgeResponse(bridge_type = asset.bridge_type,
                                                            skew_angle = asset.skew_angle,
                                                            n_spans = asset.n_spans))

        asset.set_replacement_value_model(default = True)
        asset.set_hazard_loss_model(HazusLossModel(n_spans))
        asset.set_hazard_recovery_model(SimpleRecoveryModel())
        
        
        base_idx = 19

        for i in range(FirstNetwork.n_elements):

            idx = base_idx + i*18
            
            element_name, initial_condition = asset_info[idx:idx+2]

            elem = BridgeElement(name = element_name, initial_condition = initial_condition, year = 0)
            
            p_type, X0, first_param, second_param = asset_info[idx+2:idx+6]
            elem.set_maintenance_cost_model(predictive_model(p_type, X0, first_param, second_param))
            
            p_type, X0, first_param, second_param = asset_info[idx+6:idx+10]
            elem.set_rehabilitation_cost_model(predictive_model(p_type, X0, first_param, second_param))
            
            p_type, X0, first_param, second_param = asset_info[idx+10:idx+14]
            elem.set_reconstruction_cost_model(predictive_model(p_type, X0, first_param, second_param))
            
            elem.set_condition_rating_model(Pontis_CR())
            prob_0_to_1, prob_1_to_2, prob_2_to_3, prob_3_to_4 = asset_info[idx+14:idx+18]
            elem.set_deterioration_model(Markovian_5CR(prob_0_to_1 = prob_0_to_1,
                                                            prob_1_to_2 = prob_1_to_2,
                                                            prob_2_to_3 = prob_2_to_3,
                                                            prob_3_to_4 = prob_3_to_4))
            asset.add_element(elem)
            
        return [asset]
    
    def load_network(self, n_assets = 1):
        
        assets = []
        for idx in self.assets_df.index[:n_assets]:
            assets += self.load_asset(idx)
        
        self.assets = assets
        return assets

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