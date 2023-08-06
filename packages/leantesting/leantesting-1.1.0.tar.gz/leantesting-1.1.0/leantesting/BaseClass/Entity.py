from Exception.SDKInvalidArgException import SDKInvalidArgException

class Entity:
	"""

	Represents a single Entity. All remote responses are decoded and parsed into one or more Entities.

	"""

	origin	= None # Reference to originating Client instance
	data	= None # Internal entity object data

	def __init__(self, origin, data):
		"""

		Constructs an Entity instance

		Keyword arguments:
		self   Entity   -- Self instance
		origin Client -- Original client instance reference
		data   dict     -- Data to be contained in the new Entity. Must be non-empty.

		Exceptions:
		SDKInvalidArgException if provided data param is not a dictionary.
		SDKInvalidArgException if provided data param is empty. Entities cannot be empty.

		"""

		if not isinstance(data, dict):
			raise SDKInvalidArgException('`data` must be a dictionary')
		elif not len(data):
			raise SDKInvalidArgException('`data` must be non-empty')

		self.origin = origin
		self.data   = data
