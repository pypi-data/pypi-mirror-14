from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Project.Project import Project

class ProjectsHandler(EntityHandler):

	def create(self, fields):
		super().create(fields)

		supports = {
			'name'            : True,
			'organization_id' : False
		}

		if self.enforce(fields, supports):
			req = APIRequest(self._origin, '/v1/projects', 'POST', {'params': fields})
			return Project(self._origin, req.exec_())

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/projects', 'GET')
		return EntityList(self._origin, request, Project, filters)

	def allArchived(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/projects/archived', 'GET')
		return EntityList(self._origin, request, Project, filters)

	def find(self, id_):
		super().find(id_)

		req = APIRequest(self._origin, '/v1/projects/' + str(id_), 'GET')
		return Project(self._origin, req.exec_())
