from BaseClass.EntityHandler	import EntityHandler
from BaseClass.APIRequest		import APIRequest

from Entity.Bug.BugAttachment import BugAttachment

class AttachmentsHandler(EntityHandler):

	def find(self, id_):
		super().find(id_)

		req = APIRequest(self._origin, '/v1/attachments/' + str(id_), 'GET')
		return BugAttachment(self._origin, req.exec_())

	def delete(self, id_):
		super().delete(id_)

		req = APIRequest(self._origin, '/v1/attachments/' + str(id_), 'DELETE')
		return req.exec_()
