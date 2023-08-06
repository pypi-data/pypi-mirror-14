import sys
import os
import unittest2 as unittest

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../leantesting'))

from Client import Client

from Exception.SDKInvalidArgException import SDKInvalidArgException

from Handler.Auth.OAuth2Handler				import OAuth2Handler
from Handler.User.UserHandler				import UserHandler
from Handler.Project.ProjectsHandler		import ProjectsHandler
from Handler.Bug.BugsHandler				import BugsHandler
from Handler.Attachment.AttachmentsHandler	import AttachmentsHandler
from Handler.Platform.PlatformHandler		import PlatformHandler

class ClientTest(unittest.TestCase):

	def testClientDefined(self):
		Client



	def testClientHasAuthObj(self):
		self.assertIsInstance(Client().auth, OAuth2Handler)
	def testClientHasUserObj(self):
		self.assertIsInstance(Client().user, UserHandler)
	def testClientHasProjectsObj(self):
		self.assertIsInstance(Client().projects, ProjectsHandler)
	def testClientHasBugsObj(self):
		self.assertIsInstance(Client().bugs, BugsHandler)
	def testClientHasAttachmentsObj(self):
		self.assertIsInstance(Client().attachments, AttachmentsHandler)
	def testClientHasPlatformObj(self):
		self.assertIsInstance(Client().platform, PlatformHandler)



	def testInitialEmptyToken(self):
		self.assertFalse(Client().getCurrentToken())
	def testTokenParseStorage(self):
		tokenName = '__token__test__'
		client = Client()
		client.attachToken(tokenName)
		self.assertEqual(client.getCurrentToken(), tokenName)
	def testTokenParseNonStr(self):
		self.assertRaises(SDKInvalidArgException, Client().attachToken, 7182381)



if __name__ == '__main__':
	unittest.main()
