from Exception.SDKInvalidArgException			import SDKInvalidArgException
from Exception.SDKUnsupportedRequestException	import SDKUnsupportedRequestException
from Exception.SDKIncompleteRequestException	import SDKIncompleteRequestException
from Exception.SDKDuplicateRequestException		import SDKDuplicateRequestException

class EntityHandler:
	"""

	An EntityHandler is the equivalent of a method centralizer for a corresponding endpoint (such as /v1/entities).

	Functional naming conventions and equivalents:
		create(fields)      <=>  `Create a new Entity`
		all(fields)         <=>  `List all Entities`
		find(id)            <=>  `Retrieve an existing Entity`
		delete(id)          <=>  `Delete an Entity`
		update(id, fields)  <=>  `Update an Entity`

	"""

	_origin = None # Reference to originating Client instance

	def __init__(self, origin):
		"""

		Constructs an EntityHandler instance

		Keyword arguments:
		self   EntityHandler -- Self instance
		origin Client      -- Originating client reference

		"""

		self._origin = origin

	def create(self, fields):
		"""

		Function definition for creating a new entity. Base function checks for invalid parameters.

		Keyword arguments:
		self   EntityHandler -- Self instance
		fields dict          -- Non-empty dictionary consisting of entity data to send for adding

		Exceptions:
		SDKInvalidArgException if provided fields param is not a dictionary.
		SDKInvalidArgException if provided fields param is empty.

		"""

		if not isinstance(fields, dict):
			raise SDKInvalidArgException('`fields` must be a dictionary')
		elif not len(fields):
			raise SDKInvalidArgException('`fields` must be non-empty')

	def all(self, filters = None):
		"""

		Function definition for listing all entities. Base function checks for invalid parameters.

		Keyword arguments:
		self    EntityHandler -- Self instance
		filters dict          -- (optional) Filters to apply to restrict listing. Currently supported: limit, page

		Exceptions:
		SDKInvalidArgException if provided filters param is not a dictionary.
		SDKInvalidArgException if invalid filter value found in filters dictionary.

		"""

		if filters is None:
			filters = {}

		if not isinstance(filters, dict):
			raise SDKInvalidArgException('`filters` must be a dictionary')
		else:
			for k in filters.keys():
				if not k in ['include', 'limit', 'page']:
					raise SDKInvalidArgException('unsupported ' + k + ' for `filters`')

	def find(self, id_):
		"""

		Function definition for retrieving an existing entity. Base function checks for invalid parameters.

		Keyword arguments:
		self EntityHandler -- Self instance
		id_  int           -- ID field to look for in the entity collection

		Exceptions:
		SDKInvalidArgException if provided id_ param is not an integer.

		"""

		if not isinstance(id_, int):
			raise SDKInvalidArgException('`id_` must be of type integer')

	def delete(self, id_):
		"""

		Function definition for deleting an existing entity. Base function checks for invalid parameters.

		Keyword arguments:
		self EntityHandler -- Self instance
		id_  int           -- ID field of entity to delete in the entity collection

		Exceptions:
		SDKInvalidArgException if provided id_ param is not an integer.

		"""

		if not isinstance(id_, int):
			raise SDKInvalidArgException('`id_` must be of type integer')

	def update(self, id_, fields):
		"""

		Function definition for updating an existing entity. Base function checks for invalid parameters.

		Keyword arguments:
		self   EntityHandler -- Self instance
		id_    int           -- ID field of entity to update in the entity collection
		fields dict          -- Non-empty dictionary consisting of entity data to send for update

		Exceptions:
		SDKInvalidArgException if provided id_ param is not an integer.
		SDKInvalidArgException if provided fields param is not a dictionary.
		SDKInvalidArgException if provided fields param is empty.

		"""

		if not isinstance(id_, int):
			raise SDKInvalidArgException('`id_` must be of type integer')
		elif not isinstance(fields, dict):
			raise SDKInvalidArgException('`fields` must be a dictionary')
		elif not len(fields):
			raise SDKInvalidArgException('`fields` must be non-empty')

	def enforce(self, dict_, supports):
		"""

		Helper function that enforces a structure based on a supported table:
			- Forces use of REQUIRED fields
			- Detects duplicate fields
			- Detects unsupported fields

		Keyword arguments:
		self     EntityHandler -- Self instance
		dict_    dict          -- Dictionary to be enforced
		supports dict          -- Support table consisting of REQUIRED and OPTIONAL keys to be used in enforcing

		Exceptions:
		SDKUnsupportedRequestException if unsupported fields are found
		SDKIncompleteRequestException  if any required field is missing
		SDKDuplicateRequestException   if any duplicate field is found

		"""

		sall = []				# All supported keys
		sreq = []				# Mandatory supported keys

		socc = supports.copy()	# Key use occurances

		unsup = []				# Unsupported key list
		dupl  = []				# Duplicate key list
		mreq  = []				# Missing required keys

		for sk, sv in supports.items():
			if sv == True:
				sreq.append(sk)
			sall.append(sk)
			socc[sk] = 0

		for k in dict_.keys():
			if k in sall:
				socc[k] += 1
			else:
				unsup.append(k)

		for ok, ov in socc.items():
			if ov > 1:
				dupl.append(ok)
			elif ov == 0 and ok in sreq:
				mreq.append(ok)

		if len(unsup):
			raise SDKUnsupportedRequestException(unsup)
		elif len(mreq):
			raise SDKIncompleteRequestException(mreq)
		elif len(dupl):
			raise SDKDuplicateRequestException(dupl)

		return True
