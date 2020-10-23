import numpy as np
from collections import Counter

from .BaseMRRPlan import *


class MRRFourActions(BaseMRRPlan):
	
	def __init__(self, maint_duration = 0, rehab_duration = 0, recon_duration = 0):
		super().__init__()

		self.mrr_duration = {self.MAINT: maint_duration, self.REHAB: rehab_duration, self.RECON: recon_duration}
		
		self.randomize_mrr()

	def randomize_mrr(self):
		self.mrr = np.random.randint(2, size=(self.n_elements, 2*self.dt))
		return self.mrr

	def mrr_to_decimal(self, mrr_binary = None):

		if mrr_binary is None:
			mrr = self.mrr
		else:
			mrr = mrr_binary

		self.mrr_decoded = []
		for element_idx in range (self.n_elements):
			element_mrr = []
			for j in range(0, len(mrr[element_idx]), 2):
				element_mrr.append(int(str(int(mrr[element_idx][j]*10+ mrr[element_idx][j+1])), 2))
			self.mrr_decoded.append(element_mrr)

		return self.mrr_decoded

	def mrr_to_binary(self, decoded_mrr):
		
		self.mrr = []
		for i in range(len(decoded_mrr)):
			temp_mrr = []
			for val in decoded_mrr[i]:
				for binar in bin(val)[2:]:
					temp_mrr.append(binar)
			self.mrr.append(temp_mrr)

		return self.mrr

	def check_policy(self):
		mrr_decimal = self.mrr_to_decimal()

		for elem_mrr in mrr_decimal:
			counts = Counter(elem_mrr)

			if counts[self.RECON] > 2:
				return False
			elif counts[self.REHAB] > 3:
				return False
			elif counts[self.MAINT] > 5:
				return False

		return True