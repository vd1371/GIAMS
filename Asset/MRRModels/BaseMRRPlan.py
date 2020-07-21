from utils.GeneralSettings import GenSet

class BaseMRRPlan(GenSet):
	
	def __init__(self):
		super().__init__()
		self.mrr = []

	def set_mrr(self, new_mrr):
		self.mrr = new_mrr

	def set_decoded_mrr(self, new_mrr_decoded):
		self.mrr_decoded = new_mrr_decoded

	def randomize_mrr(self):
		raise NotImplementedError ("randomly_initialize_mrr is not implemented yet")

	def mrr_to_binary(self, n):
		raise NotImplementedError ("mrr_to_binary is not implemented yet")

	def mrr_to_decimal(self, n):
		raise NotImplementedError ("mrr_to_decimal is not implemented yet")

	def check_policy(self, mrr):
		raise NotImplementedError ("check_policy of mrr is not implemented yet")

	def set_effectiveness(self, model):
		self.effectiveness = model