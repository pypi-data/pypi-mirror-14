from Exception.SDKInvalidArgException import SDKInvalidArgException

from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Bug.BugAttachment import BugAttachment

class BugAttachmentsHandler(EntityHandler):

	_bugID = None

	def __init__(self, origin, bugID):
		super().__init__(origin)

		self._bugID = bugID

	def upload(self, filepath):
		"""

		Uploads given file as an attachment for specified bug.

		Keyword arguments:
		self     BugAttachmentsHandler -- Self instance
		filepath str                   -- an absolute path of the file to be uploaded
										example: /home/path/to/file.txt (Linux), C:\\Users\\Documents\\file.txt (Windows)

		Exceptions:
		SDKInvalidArgException if filepath is not a string

		Returns:
		BugAttachment -- the newly uploaded attachment

		"""

		if not isinstance(filepath, str):
			raise SDKInvalidArgException('`filepath` must be of type string')

		req = APIRequest(
			self._origin,
			'/v1/bugs/' + str(self._bugID) + '/attachments',
			'POST',
			{
				'form_data': True,
				'file_path': filepath
			}
		)

		return BugAttachment(self._origin, req.exec_())

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/bugs/' + str(self._bugID) + '/attachments', 'GET')
		return EntityList(self._origin, request, BugAttachment, filters)
