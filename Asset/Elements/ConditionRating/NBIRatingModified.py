from .BaseConditionRating import BaseConditionRating


class NBI(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "9 Originally in NBI. As new",
									1: "8 Originally in NBI. No problem noted",
									2: "7 Originally in NBI. Some minor problems noted",
									3: "6 Originally in NBI. Structural elements show some minor deterioration.",
									4: "5 Originally in NBI. All primary structural elements are sound but may have minor section loss, cracking, spalling or scour",
									5: "4 Originally in NBI. Advanced section loss, deterioration, spalling, or scour",
									6: "3 Originally in NBI. Loss of section, deterioration, spalling or scour have seriously affected primary structural elements",
									7: "2 Originally in NBI. Advanced deterioration. Unless closely monitored it may be necessary to close the bridge until corrective action is taken"}
		
		self.ratings = [0, 1, 2, 3, 4, 5, 6, 7]
		self.reference = "IBMS Sinha"