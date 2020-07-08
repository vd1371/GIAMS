from .BaseConditionRating import BaseConditionRating


class JapanBridge_CR(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "1 Originally in the reference",
									1: "8 Originally in the reference",
									2: "7 Originally in the reference",
									3: "6 Originally in the reference"}
		self.ratings = [0, 1, 2, 3]
		self.reference = "Ministry of Land, Infrastructure, Transportation, and Tourism (2014). Manual for Bridge Periodic Inspection. Tokyo: Ministry of Land, Infrastructure, Transportation, and Tourism."