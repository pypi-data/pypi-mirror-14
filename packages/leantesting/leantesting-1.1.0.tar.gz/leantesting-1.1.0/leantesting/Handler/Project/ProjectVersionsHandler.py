from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Project.ProjectVersion import ProjectVersion

class ProjectVersionsHandler(EntityHandler):

	_projectID = None

	def __init__(self, origin, projectID):
		super().__init__(origin)

		self._projectID = projectID

	def create(self, fields):
		super().create(fields)

		supports = {
			'number': True
		}

		if self.enforce(fields, supports):
			req = APIRequest(
				self._origin,
				'/v1/projects/' + str(self._projectID) + '/versions',
				'POST',
				{'params': fields}
			)

			return ProjectVersion(self._origin, req.exec_())

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/projects/' + str(self._projectID) + '/versions', 'GET')
		return EntityList(self._origin, request, ProjectVersion, filters)
