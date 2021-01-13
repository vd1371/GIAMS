#Loading dependencies
import numpy as np

class BaseSolution:

	def __init__(self, **params):
		#Solut is a representation of a solution for the whole network
		#It represents the MRR of a network
		try:
			solut = params.pop('solut')
			self.set_solut(solut)
			self.hash_ = num_hash(self.solut)
			self.shape = np.shape(self.solut)
		except:
			self.shape = params.pop('shape')
			self.hash_ = None

		self.value = params.pop('val', -np.inf)
		self.flag = params.pop('flag', 'Regular')

	def set_value(self, val):
		self.value = val

	def set_solut(self, solut):
		self.solut = solut

	def get_solut(self):
		return np.copy(self.solut)

	def random_init(self):

		solut = []
		for n_asset in range(self.shape[0]):
			ls = []
			for n_element in range(self.shape[1]):
				num = np.random.uniform(self.lower_bound, self.upper_bound)
				arr = num_to_binary(num, self.shape)
				ls.append(arr)
			solut.append(ls)

		self.set_solut(np.array(solut))
		self.hash_ = num_hash(solut)

	def is_valid(self):
		# Only one asset exist in the solut array
		for arr in self.solut[0]:
			num = binary_to_num(arr)
			if num > self.upper_bound or num < self.lower_bound:
				return False
		return True

	def __repr__(self):
		return f"Ind {self.flag} - {self.hash_} - {self.solut} - Val:{self.value}"
	
	def __str__(self):
		return f"Ind {self.flag} - {self.hash_} - {self.solut} - Val:{self.value}"


class LCASolution(BaseSolution):
	def __init__(self, **params):
		super().__init__(**params)
		
		#LCA instance
		lca = params.pop('lca')
		self.lca_instance = lca()

		#Setting values, flag, and objective function
		self.obj_func = params.pop('obj_func', None)

		# Assign the solution vectors to the class instance
		self.set_solut_lca(self.solut)

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

	def set_solut_lca(self, solut):
		self.lca_instance.network.set_network_mrr(solut)

#-----------------------------------------------------------------------#
class DeJong(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 5.12
		self.lower_bound = -5.12

	def evaluate(self):
		if self.is_valid():
			ans = 0
			for arr in self.solut[0]:
				num = binary_to_num(arr)
				ans += num**2
			self.value = -ans
		else:
			self.value = -np.inf
#-----------------------------------------------------------------------#
class AxisParallel(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 5.12
		self.lower_bound = -5.12

	def evaluate(self):
		if self.is_valid():
			ans = 0
			for i, arr in enumerate(self.solut[0]):
				num = binary_to_num(arr)
				ans += (i+1) * num**2
			self.value = -ans
		else:
			self.value = -np.inf
#-----------------------------------------------------------------------#
class RotatedHyperEllipsoid(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 65
		self.lower_bound = -65

	def evaluate(self):
		# self.solut[0] contains an array with (validation_dimension, len_bin_array) shape
		if self.is_valid():
			ans = 0
			for i in range(len(self.solut[0])):
				for arr in self.solut[0][:i+1]:
					num = binary_to_num(arr)
					ans += num**2
			self.value = -ans
		else:
			self.value = -np.inf
#-----------------------------------------------------------------------#
class RosenbrockValley(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 2.048
		self.lower_bound = -2.048

	def evaluate(self):
		# self.solut[0] contains an array with (validation_dimension, len_bin_array) shape
		if self.is_valid():
			ans = 0
			for i in range(len(self.solut[0])-1):
				xi = binary_to_num(self.solut[0][i])
				xii = binary_to_num(self.solut[0][i+1])
				ans += 100 *(xii - xi**2)**2 + (1-xi)**2

			self.value = -ans
		else:
			self.value = -np.inf
#-----------------------------------------------------------------------#
class Rastrigin(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 5.12
		self.lower_bound = -5.12

	def evaluate(self):
		# self.solut[0] contains an array with (validation_dimension, len_bin_array) shape
		if self.is_valid():
			ans = 10 * len(self.solut[0])
			for i, arr in enumerate(self.solut[0]):
				xi = binary_to_num(arr)
				ans += xi**2 - 10*np.cos(2*np.pi*xi)
				
			self.value = -ans
		else:
			self.value = -np.inf
#-----------------------------------------------------------------------#
class Schwefel(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 500
		self.lower_bound = -500

	def evaluate(self):
		# self.solut[0] contains an array with (validation_dimension, len_bin_array) shape
		if self.is_valid():
			ans = 0
			for i, arr in enumerate(self.solut[0]):
				xi = binary_to_num(arr)
				ans += -xi * np.sin(abs(xi)**0.5)

			self.value = -ans
		else:
			self.value = -np.inf
#-----------------------------------------------------------------------#
class Griewangk(BaseSolution):

	def __init__(self, **params):
		super().__init__(**params)
		# NOTE: lower and upper bound should be within
		#	-100 and 100 for validation_dimension == 4
		#	-1000 and 1000 for validation_dimension == 3
		# Don't ask why :), it's for simplicity of validation
		self.upper_bound = 600
		self.lower_bound = -600

	def evaluate(self):
		# self.solut[0] contains an array with (validation_dimension, len_bin_array) shape
		if self.is_valid():
			ans1 = 0
			for i, arr in enumerate(self.solut[0]):
				xi = binary_to_num(arr)
				ans1 += 1/4000*xi**2

			ans2 = 1
			for i, arr in enumerate(self.solut[0]):
				xi = binary_to_num(arr)
				ans2 = ans2 * np.cos(xi / (i+1)**0.5)
			
			ans = ans1 - ans2 + 1

			self.value = -ans
		else:
			self.value = -np.inf
	
#-----------------------------------------------------------------------#
#
# Some useful functions
#
#-----------------------------------------------------------------------#

# Creating a local function for to evaluate the individuals
def _eval_sol(sol):
	'''Helper function for parallel processing

	This function will be used for mapping it to a list of
	solution for parallel processing in optimization problems 
	'''
	sol.evaluate()
	return sol

def num_to_binary(num, shape):
	'''Converts numbers to binary arrays with length of shape[2]'''
	num = int(num * 100)
	result = [(num>>k)&1 for k in range(0, shape[2])]
	result.reverse()
	return np.array(result)

def binary_to_num(arr):
	'''Converts binary arrays to numbers
	
	The underlying assumption in validation is that the accuracy
	of results will be by 2 decimal points
	The arr shape is like: (n_assets, n_elements, mrr_for_element)
	'''
	out_str = ""
	for val in arr:
		out_str += str(val)
	return int(out_str, 2) / 100

def num_hash(arr):
	'''Hash function for taboo checking

	It is basically the string representation of the number
	equivalent to the binary array
	'''
	out_str = ""
	for ar in arr:
		for a in ar:
			out_str += str(binary_to_num(a)) + "-"

	return out_str[:-1]


if __name__ == "__main__":

	test =  num_to_binary(9696, 15)
	print (test)
	print (binary_to_num(test))

