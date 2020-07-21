from .BaseUserCostModel import BaseUserCostModel

from utils.PredictiveModels.Linear import Linear

class TexasDOTUserCost(BaseUserCostModel):

	def __init__(self, speed_before = 60,
						speed_after = 30):
		super().__init__()

		self.speed_before = speed_before
		self.speed_after = speed_after
		self.detour_usage_percentage = 0.1

		self.linear_model = Linear(1, 0)

	def set_detour_usage_percentage(self, val):
		self.detour_usage_percentage = val

	def predict_series(self, project_duration, random = True):

		# These values are based on dollars
		vehicle_value_of_time = 30.12 * self.linear_model.predict_series(random, "TexasDOTUserCost")
		vehicle_value_per_mile = 0.741* self.linear_model.predict_series(random, "TexasDOTUserCost")
		vehicle_marginal_cost_per_mile = 0.0962 * self.linear_model.predict_series(random, "TexasDOTUserCost")

		truck_value_of_time = 41.33 * self.linear_model.predict_series(random, "TexasDOTUserCost")
		truck_value_per_mile = 1.022 * self.linear_model.predict_series(random, "TexasDOTUserCost")
		truck_marginal_cost_per_mile = 0.3137 * self.linear_model.predict_series(random, "TexasDOTUserCost")

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
