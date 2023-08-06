from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Project.ProjectBugScheme import ProjectBugScheme

class ProjectBugTypeSchemeHandler(EntityHandler):

	_projectID = None

	def __init__(self, origin, projectID):
		super().__init__(origin)

		self._projectID = projectID

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/projects/' + str(self._projectID) + '/bug-type-scheme', 'GET')
		return EntityList(self._origin, request, ProjectBugScheme, filters)
