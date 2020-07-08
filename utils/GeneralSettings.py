# Management settings
import numpy as np

class GenSet(object):

	n_simulations = 1
	n_elements = 4
	n_states = 5
	dt = 2
	horizon = 6
	discount_rate = 0.04


	init_year = 0
	n_steps = int(horizon/dt) + 1
	DONOT = 0
	MAINT = 1
	REHAB = 2
	RECON = 3