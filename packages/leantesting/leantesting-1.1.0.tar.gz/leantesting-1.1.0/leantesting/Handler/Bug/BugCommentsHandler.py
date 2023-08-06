from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Bug.BugComment import BugComment

class BugCommentsHandler(EntityHandler):

	_bugID = None

	def __init__(self, origin, bugID):
		super().__init__(origin)

		self._bugID = bugID

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/bugs/' + str(self._bugID) + '/comments', 'GET')
		return EntityList(self._origin, request, BugComment, filters)
