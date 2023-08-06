from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Handler.User.UserOrganizationsHandler import UserOrganizationsHandler

class UserHandler(EntityHandler):

	organizations = None

	def __init__(self, origin):
		super().__init__(origin)

		self.organizations = UserOrganizationsHandler(origin)

	def getInformation(self):
		return (APIRequest(self._origin, '/v1/me', 'GET')).exec_()
