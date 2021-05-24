#Loading dependencies

class BaseEnv:
	def __init__(self, **params):
		'''Constructor method for the BaseEnv object
		
		This is the base class for future Envs in GIAMS. To keep
		the repository consistent with the OpenAi gyms, all future
		envs should contain three methods like the BaseEnv
		'''
		self.settings = params.pop("settings", None)

	def reset(self):
		'''Resetting the env
		
		:return: the initial state of the whole environment
		'''
		raise NotImplementedError ("reset method is not implemented yet")

	def step(self, action):
		'''Taking a step in the env

		:params: action: the action that needs to be taken
		:return: new_state, reward, done, info
		'''
		raise NotImplementedError ("step method is not implemented yet")