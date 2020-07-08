from .BaseConditionRating import BaseConditionRating


class ChinaHighwayBridges_CR(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "1 Originally in the reference. No corrosion",
									1: "2 Originally in the reference. Paint distress",
									2: "3 Originally in the reference. Rust formation",
									3: "4 Originally in the reference. Active corrosion",
									4: "5 Originally in the reference. Section loss"}
		self.ratings = [0, 1, 2, 3, 4]
		self.reference = "Standards for technical condition evaluation of Highway Bridges, Jtg/t-H21–2011, 2011"