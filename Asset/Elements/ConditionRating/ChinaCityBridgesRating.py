from .BaseConditionRating import BaseConditionRating


class ChinaCityBridges_CR(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "A Originally in the reference. No corrosion",
									1: "B Originally in the reference. Paint distress",
									2: "C Originally in the reference. Rust formation",
									3: "D Originally in the reference. Active corrosion",
									4: "E Originally in the reference. Section loss"}
		self.ratings = [0, 1, 2, 3, 4]
		self.reference = "technical code of Maintenance for city Bridge, cJJ99–2003, 2003"
