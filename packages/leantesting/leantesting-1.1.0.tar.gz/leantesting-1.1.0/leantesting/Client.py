import sys
import os

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from Exception.SDKInvalidArgException import SDKInvalidArgException

from Handler.Auth.OAuth2Handler				import OAuth2Handler
from Handler.User.UserHandler				import UserHandler
from Handler.Project.ProjectsHandler		import ProjectsHandler
from Handler.Bug.BugsHandler				import BugsHandler
from Handler.Attachment.AttachmentsHandler	import AttachmentsHandler
from Handler.Platform.PlatformHandler		import PlatformHandler

class Client:
	"""

	Lean Testing Python Client SDK

	https://leantesting.com/en/api-docs Adheres to official API guidelines

	"""

	_accessToken  = None

	auth		= None
	user		= None
	projects	= None
	bugs		= None
	attachments	= None
	platform	= None

	debugReturn = None

	def __init__(self):
		"""

		Constructs a Client instance

		Keyword arguments:
		self Client -- Self instance

		"""

		self.auth			= OAuth2Handler(self)
		self.user			= UserHandler(self)
		self.projects		= ProjectsHandler(self)
		self.bugs			= BugsHandler(self)
		self.attachments	= AttachmentsHandler(self)
		self.platform		= PlatformHandler(self)

	def getCurrentToken(self):
		"""

		Function to retrieve curently attached token.

		Keyword arguments:
		self Client -- Self instance

		Returns:
		str     -- if a token is attached
		boolean -- if no token is attached

		"""

		if self._accessToken is None:
			return False

		return self._accessToken

	def attachToken(self, accessToken):
		"""

		Function to attach new token to SDK Client instance. Token changes are dynamic; all objects/entities
		originating from an instance which has had its token updated will utilize the new token automatically.

		Keyword arguments:
		self        Client -- Self instance
		accessToken str      -- the string of the token to be attached

		Exceptions:
		SDKInvalidArgException if provided accessToken param is not a string

		"""

		if not isinstance(accessToken, str):
			raise SDKInvalidArgException('`accessToken` must be a string')

		self._accessToken = accessToken
