from .BaseConditionRating import BaseConditionRating


class NBI_CR(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "9 Originally in NBI. As new",
									1: "8 Originally in NBI. No problem noted",
									2: "7 Originally in NBI. Some minor problems noted",
									3: "6 Originally in NBI. Structural elements show some minor deterioration.",
									4: "5 Originally in NBI. All primary structural elements are sound but may have minor section loss, cracking, spalling or scour",
									5: "4 Originally in NBI. Advanced section loss, deterioration, spalling, or scour",
									6: "3 Originally in NBI. Loss of section, deterioration, spalling or scour have seriously affected primary structural elements",
									7: "2 Originally in NBI. Advanced deterioration. Unless closely monitored it may be necessary to close the bridge until corrective action is taken",
									8: "1 Originally in NBI. Major deterioration. Bridge is closed but corrective action may put back in light service",
									9: "0 Originally in NBI. Bridge is out of service. Beyond conrrective action"}
		
		self.ratings = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.reference = "FHWA (Federal Highway Administration). (1995). Recording and coding guide for the structure inventory and appraisal of the nation’s bridges. Washington, DC."