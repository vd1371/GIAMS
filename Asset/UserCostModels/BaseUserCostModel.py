from utils.GeneralSettings import GenSet


class BaseUserCostModel(GenSet):

	def __init__(self):
		super().__init__()

	def predict_series(self):
		raise NotImplementedError ("predict_series of user cost model is not implemented yet")
