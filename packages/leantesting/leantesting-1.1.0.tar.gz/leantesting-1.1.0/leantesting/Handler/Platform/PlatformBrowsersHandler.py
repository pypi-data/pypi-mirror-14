from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Platform.PlatformBrowser import PlatformBrowser

class PlatformBrowsersHandler(EntityHandler):

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		initFilters = {'include': 'versions'}
		initFilters.update(filters)
		filters = initFilters

		request = APIRequest(self._origin, '/v1/platform/browsers', 'GET')
		return EntityList(self._origin, request, PlatformBrowser, filters)

	def find(self, id_):
		super().find(id_)

		req = APIRequest(self._origin, '/v1/platform/browsers/' + str(id_), 'GET', {'params': {'include': 'versions'}})
		return PlatformBrowser(self._origin, req.exec_())
