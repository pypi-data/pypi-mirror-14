from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Platform.PlatformDevice import PlatformDevice

class PlatformTypeDevicesHandler(EntityHandler):

	_typeID = None

	def __init__(self, origin, typeID):
		super().__init__(origin)

		self._typeID = typeID

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/platform/types/' + str(self._typeID) + '/devices', 'GET')
		return EntityList(self._origin, request, PlatformDevice, filters)
