# Management settings
import numpy as np

### Elements name
SUPERSTRUCTURE = 'Superstructure'
SUBSTRUCTURE = 'Substructure'
DECK = 'Deck'
WEARING = 'Wearing Surface'
ARCH = 'Arch'
JOINT = 'Joint'
PATCHING = 'Patching'

### Material
STEEL = 'Steel'
TIMBER = 'Timber'

#### Road type
NHS = 'NHS'
MAJOR = 'Major'
MINOR = 'Minor'
LOCAL = 'Local'

class GenSet(object):

	n_simulations = 10
	n_elements = 3
	n_states = 8
	dt = 2
	horizon = 10
	discount_rate = 0.0

	init_year = 0
	n_steps = int(horizon/dt) + 1

	DONOT = 0
	MAINT = 1
	REHAB = 2
	RECON = 3
	