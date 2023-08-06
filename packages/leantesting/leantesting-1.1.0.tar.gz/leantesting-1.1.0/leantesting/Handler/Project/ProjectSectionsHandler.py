from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Project.ProjectSection import ProjectSection

class ProjectSectionsHandler(EntityHandler):

	_projectID = None

	def __init__(self, origin, projectID):
		super().__init__(origin)

		self._projectID = projectID

	def create(self, fields):
		super().create(fields)

		supports = {
			'name': True
		}

		if self.enforce(fields, supports):
			req = APIRequest(
				self._origin,
				'/v1/projects/' + str(self._projectID) + '/sections',
				'POST',
				{'params': fields}
			)

			return ProjectSection(self._origin, req.exec_())

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/projects/' + str(self._projectID) + '/sections', 'GET')
		return EntityList(self._origin, request, ProjectSection, filters)
