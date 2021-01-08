from .BaseUserCost import BaseUserCost

from utils.PredictiveModels.Linear import Linear
from utils.PredictiveModels.WienerDrift import WienerDrift

class TexasDOTUserCostWithVolatility(BaseUserCost):

	def __init__(self, **params):
		super().__init__(**params)

		self.speed_before = params.pop('speed_before', 60)
		self.speed_after = params.pop('speed_after', 30)
		self.detour_usage_percentage = params.pop('detour_usage_percentage', 0.1)
		volatility = params.pop('volatility', 0.01)
		drift = params.pop('drift', 0.1)

		val = 30.12
		self.vehicle_value_of_time = WienerDrift(val, val*drift, val*volatility)

		val = 0.741
		self.vehicle_value_per_mile = WienerDrift(val, val*drift, val*volatility)

		val = 0.0962
		self.vehicle_marginal_cost_per_mile = WienerDrift(val, val*drift, val*volatility)

		val = 41.33
		self.truck_value_of_time = WienerDrift(val, val*drift, val*volatility)
		
		val = 1.022
		self.truck_value_per_mile = WienerDrift(val, val*drift, val*volatility)
		
		val = 0.3137
		self.truck_marginal_cost_per_mile = WienerDrift(val, val*drift, val*volatility)

	def set_detour_usage_percentage(self, val):
		self.detour_usage_percentage = val

	def predict_series(self, project_duration, random = True):

		# These values are based on dollars
		vehicle_value_of_time = self.vehicle_value_of_time.predict_series(random, "TexDOTWithVolatility")
		vehicle_value_per_mile = self.vehicle_value_per_mile.predict_series(random, "TexDOTWithVolatility")
		vehicle_marginal_cost_per_mile = self.vehicle_marginal_cost_per_mile.predict_series(random, "TexDOTWithVolatility")

		truck_value_of_time = self.truck_value_of_time.predict_series(random, "TexDOTWithVolatility")
		truck_value_per_mile = self.truck_value_per_mile.predict_series(random, "TexDOTWithVolatility")
		truck_marginal_cost_per_mile = self.truck_marginal_cost_per_mile.predict_series(random, "TexDOTWithVolatility")

		# For those who uses the bridge
		trucks = int (self.asset.ADT*(1 - self.detour_usage_percentage) * self.asset.truck_percentage) 
		vehicles = self.asset.ADT*(1 - self.detour_usage_percentage) - trucks

		delay = self.asset.length/self.speed_after - self.asset.length/self.speed_before # In minutes
		delay_cost = delay / 60 * (vehicles * vehicle_value_of_time + trucks * truck_value_of_time) # per hour
		marginal_cost = (vehicles * vehicle_marginal_cost_per_mile + trucks * truck_marginal_cost_per_mile) * self.asset.length / 1609 # meter to mile

		# For those who uses the detour
		trucks = int (self.asset.ADT * self.detour_usage_percentage * self.asset.truck_percentage) 
		vehicles = self.asset.ADT * self.detour_usage_percentage - trucks

		operating_cost = (vehicles * vehicle_value_per_mile + trucks * truck_value_per_mile) * self.asset.detour_length
		travel_cost = self.asset.detour_length / self.speed_before * (vehicles * vehicle_value_of_time + trucks * truck_value_of_time)

		return (delay_cost + marginal_cost + operating_cost + travel_cost) * project_duration / 1000
