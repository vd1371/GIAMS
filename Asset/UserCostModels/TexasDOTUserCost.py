from .BaseUserCostModel import BaseUserCostModel

from utils.PredictiveModels.Linear import Linear

class TexasDOTUserCost(BaseUserCostModel):

	def __init__(self, ADT = 1000,
						percent_truck = 0,
						speed_before = 0,
						speed_after = 0,
						segment_length = 0,
						detour_length = 0,
						detour_usage_percentage = 0):
		super().__init__()

		self.ADT = ADT
		self.percent_truck = percent_truck
		self.speed_before = speed_before
		self.speed_after = speed_after
		self.detour_length = detour_length
		self.detour_usage_percentage = detour_usage_percentage
		self.segment_length = segment_length

	def predict_series(self, project_duration):

		# These values are based on dollars
		vehicle_value_of_time = Linear(30.12, 1.8).predict_series()
		vehicle_value_per_mile = Linear(0.741, 0.04).predict_series()
		vehicle_marginal_cost_per_mile = Linear (0.0962, 0.005).predict_series()

		truck_value_of_time = Linear(41.33, 2.5).predict_series()
		truck_value_per_mile = Linear(1.022, 0.05).predict_series()
		truck_marginal_cost_per_mile = Linear (0.3137, 0.05).predict_series()

		# For those who uses the bridge
		trucks = int (self.ADT*(1 - self.detour_usage_percentage) * self.percent_truck) 
		vehicles = self.ADT*(1 - self.detour_usage_percentage) - trucks

		delay = self.segment_length/self.speed_after - self.segment_length/self.speed_before # In minutes
		delay_cost = delay / 60 * (vehicles * vehicle_value_of_time + trucks * truck_value_of_time) # per hour
		marginal_cost = (vehicles * vehicle_marginal_cost_per_mile + trucks * truck_marginal_cost_per_mile) * self.segment_length

		# For those who uses the detour
		trucks = int (self.ADT * self.detour_usage_percentage * self.percent_truck) 
		vehicles = self.ADT * self.detour_usage_percentage - trucks

		operating_cost = (vehicles * vehicle_value_per_mile + trucks * truck_value_per_mile) * self.detour_length
		travel_cost = self.detour_length / self.speed_before * (vehicles * vehicle_value_of_time + trucks * truck_value_of_time)

		return (delay_cost + marginal_cost + operating_cost + travel_cost) * project_duration / 1000000
