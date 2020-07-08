from .BaseConditionRating import BaseConditionRating


class Pontis_CR(BaseConditionRating):

	def __init__(self):
		super().__init__()

		self.ratings_description = {0: "1 Originally in PONTIS. No corrosion",
									1: "2 Originally in PONTIS. Paint distress",
									2: "3 Originally in PONTIS. Rust formation",
									3: "4 Originally in PONTIS. Active corrosion",
									4: "5 Originally in PONTIS. Section loss"}
		self.ratings = [0, 1, 2, 3, 4]
		self.reference = "Thompson, P. D., P.Small, E., Johnson, M., and R.Marshal, A. (1998). “The Pontis bridge management system.” Structural engineering international, 8(4), 303–308"


if __name__ == "__main__":
	pontis = PONTIS_CR()
	print (pontis)