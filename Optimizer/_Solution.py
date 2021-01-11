#Loading dependencies
import numpy as np

class Solution:
	def __init__(self, **params):
		
		#LCA instance
		lca = params.pop('lca')
		self.lca_instance = lca()

		#Solut is a representation of a solution for the whole network
		#It represents the MRR of a network
		solut = params.pop('solut', None)
		self.set_solut(solut)
		self.hash_ = hash(self.solut.tostring())

		#Setting values, flag, and objective function
		self.value = params.pop('val', -np.inf)
		self.flag = params.pop('flag', 'Regular')
		self.obj_func = params.pop('obj_func', None)

	def evaluate(self):
		'''Evaluate method of the solution'''
		#Running the LCA
		self.lca_instance.run()

		#Check the budget  
		if self.lca_instance.check_budget():
			user_costs, agency_costs, utilities = self.lca_instance.get_network_npv()
			self.value = self.obj_func (UserCost = user_costs,
										AgencyCost = agency_costs,
										Utility = utilities)

		#If not in the budget, set a negative amount as the objective value
		else:
			self.value = -1000

	def is_valid(self):
		'''See if the solution meets the policies'''
		for asset in self.lca_instance.network.assets:
			if not asset.mrr_model.check_policy():
				# To check whether the mrr meets certain policies
				# For example only two reconstrcution for an element in the horizon
				return False

		return True

	def set_value(self, val):
		self.value = val

	def set_solut(self, solut):
		self.solut = solut
		self.lca_instance.network.set_network_mrr(solut)

	def get_solut(self):
		return np.copy(self.solut)

	def __repr__(self):
		return f"Ind {self.flag} - {self.hash_} - {self.solut} - Val:{self.value}"
	
	def __str__(self):
		return f"Ind {self.flag} - {self.hash_} - {self.solut} - Val:{self.value}"

# Creating a local function for to evaluate the individuals
def _eval_sol(ind):
	sol.evaluate()
	return sol