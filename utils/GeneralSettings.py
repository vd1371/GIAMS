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

	n_elements = 1
	n_states = 8
	dt = 1
	horizon = 50
	discount_rate = 0.03

	init_year = 0
	n_steps = int(horizon/dt)
	
	DONOT = 0
	MAINT = 1
	REHAB = 2
	RECON = 3
	BINAR = 1
	