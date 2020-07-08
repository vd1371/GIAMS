

class BaseDeteriorationModel(object):

	def __init__(self):
		super(BaseDeteriorationModel, self).__init__()

	def predict_condition(self, previous_condition = None, age = None):
		raise NotImplementedError ("The predict_condition method is not implemented yet")