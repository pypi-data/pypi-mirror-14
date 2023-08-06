from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Platform.PlatformType import PlatformType

class PlatformTypesHandler(EntityHandler):

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/platform/types', 'GET')
		return EntityList(self._origin, request, PlatformType, filters)

	def find(self, id_):
		super().find(id_)

		req = APIRequest(self._origin, '/v1/platform/types/' + str(id_), 'GET')
		return PlatformType(self._origin, req.exec_())
