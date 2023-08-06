from Exception.SDKUnexpectedResponseException import SDKUnexpectedResponseException

class EntityList:
	"""

	An EntityList is a list of Entity objects, obtained from compiling the results of an all() call.

	"""

	_origin     = None # Reference to originating Client instance

	_identifier = None # Class definition identifier for the collection Entities
	_collection = None # Internal collection corresponding to current page

	_request    = None # APIRequest definition to use for collection generation
	_filters    = None # Filter list for generation (origins in Handler call)

	_pagination = None # Pagination object as per response (without links)
	_realPage   = None # Effective virtual paginator for out-of-bounds scenarios

	def _generateCollectionData(self):
		"""

		(Re)generates internal collection data based on current iteration position.

		Regeneration is done every time position changes (i.e. every time repositioning functions are used).

		Keyword arguments:
		self EntityList -- Self instance

		Exceptions:
		SDKUnexpectedResponseException if no `meta` field is found
		SDKUnexpectedResponseException if no `pagination` field is found in `meta field`
		SDKUnexpectedResponseException if no collection set is found
		SDKUnexpectedResponseException if multiple collection sets are found

		"""

		self._collection = [] # Clear previous collection data on fresh regeneration
		self._pagination = {} # Clear previous pagination data on fresh regeneration

		self._request.updateOpts({'params': self._filters})
		raw = self._request.exec_()

		if not 'meta' in raw.keys():
			raise SDKUnexpectedResponseException('missing `meta` field')
		elif not 'pagination' in raw['meta'].keys():
			raise SDKUnexpectedResponseException('`meta` missing `pagination` field')

		if 'links' in raw['meta']['pagination']:
			raw['meta']['pagination'].pop('links')		# Remove not needed links sub-data

		self._pagination = raw['meta']['pagination']	# Pass pagination data as per response meta key
		raw.pop('meta')

		if not len(raw):
			raise SDKUnexpectedResponseException('collection object missing')
		elif len(raw) > 1:
			cols = ', '.join(raw.keys())
			raise SDKUnexpectedResponseException('expected one collection object, multiple received: ' + cols)

		classDef = self._identifier # Definition to be used for dynamic Entity instancing
		for entity in next(iter(raw.values())):
			self._collection.append(classDef(self._origin, entity))

	def __init__(self, origin, request, identifier, filters = None):
		"""

		Constructs an Entity List instance.

		Keyword arguments:
		self       EntityList -- Self instance
		origin     Client   -- Original client instance reference
		request    APIRequest -- An API Request definition given by the entity collection handler. This is used for any
							subsequent collection regeneration, as any data updates are dependant on external requests.
		identifier class      -- class definition to use for dynamic class instancing within list collection
		filters    dict       -- original filters passed over from originating all() call

		"""

		if filters is None:
			filters = {}

		self._origin     = origin
		self._request    = request
		self._identifier = identifier
		self._filters    = filters

		if 'page' in filters.keys():
			self._realPage = filters['page']
		else:
			self._realPage = 1

		self._generateCollectionData()

	def first(self):
		"""

		Sets iterator position to first page. Ignored if already on first page.

		Keyword arguments:
		self EntityList -- Self instance

		"""

		if self._pagination['current_page'] == 1:
			return False

		self._filters['page'] = 1
		self._generateCollectionData()
		self._realPage = 1

	def previous(self):
		"""

		Sets iterator position to previous page. Ignored if on first page.

		Keyword arguments:
		self EntityList -- Self instance

		"""

		if self._pagination['current_page'] == 1:
			return False

		self._filters['page'] -= 1
		self._generateCollectionData()
		self._realPage -= 1

	def next(self):
		"""

		Sets iterator position to next page. Ignored if on last page.
		(required for iterator implementation)

		Keyword arguments:
		self EntityList -- Self instance

		Exceptions:
		StopIteration if forward bounds are reached

		"""

		if self._pagination['current_page'] == self._pagination['total_pages']:
			return False

		if 'page' in self._filters.keys():
			self._filters['page'] += 1
		else:
			self._filters['page']  = 2

		self._generateCollectionData()
		self._realPage += 1

	def __next__(self):
		"""

		Internal equivalent of next(), to be used in iteration loops
		(required for iterator implementation)

		Keyword arguments:
		self EntityList -- Self instance

		"""

		if  self._realPage > self._pagination['total_pages']:
			raise StopIteration

		ret = self.toArray()

		if not self._pagination['current_page'] == self._pagination['total_pages']:
			if 'page' in self._filters.keys():
				self._filters['page'] += 1
			else:
				self._filters['page']  = 2

			self._generateCollectionData()

		self._realPage += 1

		return ret

	def last(self):
		"""

		Sets iterator position to last page. Ignored if already on last page.

		Keyword arguments:
		self EntityList -- Self instance

		"""

		if self._pagination['current_page'] == self._pagination['total_pages']:
			return False

		self._filters['page'] = self._pagination['total_pages']
		self._generateCollectionData()
		self._realPage = self._pagination['total_pages']

	def __iter__(self):
		"""

		Returns the Entity collection for the current page.
		(required for iterator implementation)

		Keyword arguments:
		self EntityList -- Self instance

		Returns:
		list -- internal collection of Entity objects. Objects will be of child class types, not Entity parent.

		"""

		self.first()
		return self

	def total(self):
		"""

		Outputs total number of Entities inside multi-page collection

		Keyword arguments:
		self EntityList -- Self instance

		Returns:
		int -- Number of total Entities

		"""

		return self._pagination['total']

	def totalPages(self):
		"""

		Outputs total number of pages the multi-page collection has, regardful of limit/per_page

		Keyword arguments:
		self EntityList -- Self instance

		Returns:
		int -- Number of total pages

		"""

		return self._pagination['total_pages']

	def count(self):
		"""

		Outputs number of Entities in current collection page. Will always be same as limmit/per_page if not on last page.

		Keyword arguments:
		self EntityList -- Self instance

		Returns:
		int -- Number of Entities in page

		"""

		return self._pagination['count']

	def toArray(self):
		"""

		Outputs internal collection in array format (converted from Entity objects)

		Keyword arguments:
		self EntityList -- Self instance

		Returns:
		list -- list of elements converted into dictionaries

		"""

		arr = []
		for entity in self._collection:
			arr.append(entity.data)

		return arr
