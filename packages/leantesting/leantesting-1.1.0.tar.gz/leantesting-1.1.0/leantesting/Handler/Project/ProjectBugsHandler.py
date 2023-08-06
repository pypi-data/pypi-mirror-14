from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Bug.Bug import Bug

class ProjectBugsHandler(EntityHandler):

	_projectID = None

	def __init__(self, origin, projectID):
		super().__init__(origin)

		self._projectID = projectID

	def create(self, fields):
		super().create(fields)

		supports = {
			'title'              : True,
			'status_id'          : True,
			'severity_id'        : True,
			'project_version'    : True,
			'project_version_id' : True,
			'project_section_id' : False,
			'type_id'            : False,
			'reproducibility_id' : False,
		   	'priority_id'		 : False,
			'assigned_user_id'   : False,
			'description'        : False,
			'expected_results'   : False,
			'steps'              : False,
			'platform'           : False
			# 'device_model'       : False,
			# 'device_model_id'    : False,
			# 'os'                 : False,
			# 'os_version'         : False,
			# 'os_version_id'      : False,
			# 'browser_version_id' : False
		}

		if 'project_version_id' in fields.keys():
			supports['project_version'] = False
		elif 'project_version' in fields.keys():
			supports['project_version_id'] = False

		if self.enforce(fields, supports):
			initFields = {'include': 'steps,platform'}
			initFields.update(fields)
			fields = initFields

			req = APIRequest(
				self._origin,
				'/v1/projects/' + str(self._projectID) + '/bugs',
				'POST',
				{'params': fields}
			)

			return Bug(self._origin, req.exec_())

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		initFilters = {'include': 'steps,platform,attachments,comments,tags'}
		initFilters.update(filters)
		filters = initFilters

		request = APIRequest(self._origin, '/v1/projects/' + str(self._projectID) + '/bugs', 'GET')
		return EntityList(self._origin, request, Bug, filters)
