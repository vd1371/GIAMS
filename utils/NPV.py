# Management settings
import numpy as np

def NPV(costs_list, dt, r = 0.06):
	val = 0
	for i, cost in enumerate(costs_list):
		val += np.exp(-r*dt*i) * cost
	return val