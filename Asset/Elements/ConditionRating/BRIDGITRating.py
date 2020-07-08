from .BaseConditionRating import BaseConditionRating


class BRIDGIT_CR(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "1 Originally in BRIDGIT. No signs of cracking",
									1: "8 Originally in BRIDGIT. Minor deterioration",
									2: "7 Originally in BRIDGIT. Medium detrioration exists",
									3: "6 Originally in BRIDGIT. Advanced detrioration to concrete surfaces"}
		self.ratings = [0, 1, 2, 3]
		self.reference = "Hawk, H., and Small, E. P. (1998). “The BRIDGIT bridge management system.” Structural Engineering International: Journal of the International Association for Bridge and Structural Engineering (IABSE), 8(4), 309–314."