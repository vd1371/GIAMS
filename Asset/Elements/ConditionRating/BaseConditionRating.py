import pprint


class BaseConditionRating(object):
	'''
	This is the base class for the condition rating modules
	All CR modlues should inherit from this class
	The discrete condition ratings should be in an increasing manner. For example, lower ratings should
	...indicate better condition. This is a MUST for deterioration modelling
	
	To see how these ratings could be mapped to each other:
	
	Yoseok Jeong, WooSeok Kim, Ilkeun Lee & Jaeha Lee (2018) Bridge
	inspection practices and bridge management programs in China, Japan, Korea, and U.S., Journal
	of Structural Integrity and Maintenance, 3:2, 126-135, DOI: 10.1080/24705314.2018.1461548
	'''


	def __init__(self):
		
		super().__init__()
		self.ratings_description = None
		self.ratings = None
		self.reference= "Not specified"

	def __str__(self):
		return "\nThis description might not be accurate. Please refer to the reference for further information\n" + pprint.pformat(self.ratings_description) + "\nRef:" + self.reference

