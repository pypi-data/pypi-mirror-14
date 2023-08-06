import sys
import os

import unittest2 as unittest

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../leantesting'))

from Client import Client

from Exception.SDKInvalidArgException import SDKInvalidArgException

from BaseClass.Entity	import Entity

from Entity.Bug.Bug				import Bug
from Entity.Bug.BugAttachment	import BugAttachment
from Entity.Bug.BugComment		import BugComment

from Entity.Platform.PlatformBrowser		import PlatformBrowser
from Entity.Platform.PlatformBrowserVersion	import PlatformBrowserVersion
from Entity.Platform.PlatformDevice			import PlatformDevice
from Entity.Platform.PlatformOS				import PlatformOS
from Entity.Platform.PlatformOSVersion		import PlatformOSVersion
from Entity.Platform.PlatformType			import PlatformType

from Entity.Project.Project					import Project
from Entity.Project.ProjectBugScheme		import ProjectBugScheme
from Entity.Project.ProjectSection			import ProjectSection
from Entity.Project.ProjectUser				import ProjectUser
from Entity.Project.ProjectVersion			import ProjectVersion

from Entity.User.UserOrganization	import UserOrganization

from Handler.Bug.BugCommentsHandler		import BugCommentsHandler
from Handler.Bug.BugAttachmentsHandler	import BugAttachmentsHandler

from Handler.Platform.PlatformBrowserVersionsHandler	import PlatformBrowserVersionsHandler
from Handler.Platform.PlatformOSVersionsHandler			import PlatformOSVersionsHandler
from Handler.Platform.PlatformTypeDevicesHandler		import PlatformTypeDevicesHandler

from Handler.Project.ProjectSectionsHandler	import ProjectSectionsHandler
from Handler.Project.ProjectVersionsHandler	import ProjectVersionsHandler
from Handler.Project.ProjectUsersHandler	import ProjectUsersHandler

from Handler.Project.ProjectBugTypeSchemeHandler			import ProjectBugTypeSchemeHandler
from Handler.Project.ProjectBugStatusSchemeHandler			import ProjectBugStatusSchemeHandler
from Handler.Project.ProjectBugSeveritySchemeHandler		import ProjectBugSeveritySchemeHandler
from Handler.Project.ProjectBugReproducibilitySchemeHandler	import ProjectBugReproducibilitySchemeHandler
from Handler.Project.ProjectBugPrioritySchemeHandler		import ProjectBugPrioritySchemeHandler

from Handler.Project.ProjectBugsHandler	import ProjectBugsHandler

class EntitiesTest(unittest.TestCase):

	_entityColllection = [
		[Bug, {
			'comments'      : BugCommentsHandler,
			'attachments'   : BugAttachmentsHandler
		}],
		[BugAttachment],
		[BugComment],
		[PlatformBrowser, {
			'versions'      : PlatformBrowserVersionsHandler
		}],
		[PlatformBrowserVersion],
		[PlatformDevice],
		[PlatformOS, {
			'versions'      : PlatformOSVersionsHandler
		}],
		[PlatformOSVersion],
		[PlatformType, {
			'devices'       : PlatformTypeDevicesHandler
		}],
		[Project, {
			'sections'      : ProjectSectionsHandler,
			'versions'      : ProjectVersionsHandler,
			'users'         : ProjectUsersHandler,

			'bugTypeScheme'             : ProjectBugTypeSchemeHandler,
			'bugStatusScheme'           : ProjectBugStatusSchemeHandler,
			'bugSeverityScheme'         : ProjectBugSeveritySchemeHandler,
			'bugReproducibilityScheme'  : ProjectBugReproducibilitySchemeHandler,
			'bugPriorityScheme'  		: ProjectBugPrioritySchemeHandler,

			'bugs'          : ProjectBugsHandler
		}],
		[ProjectBugScheme],
		[ProjectSection],
		[ProjectUser],
		[ProjectVersion],
		[UserOrganization]
	]


	def testEntitiesDefined(self):
		for e in self._entityColllection:
			e[0]

	def testEntitiesCorrectParent(self):
		for e in self._entityColllection:
			self.assertIsInstance(e[0](Client(), {'id': 1}), Entity)

	def testEntitiesDataParsing(self):
		data = {'id': 1, 'YY': 'strstr', 'FF': [1, 2, 3, 'asdasdasd'], 'GG': {'test1': True, 'test2': []}}
		for e in self._entityColllection:
			self.assertIs((e[0](Client(), data)).data, data)



	def testEntitiesInstanceNonArrData(self):
		for e in self._entityColllection:
			self.assertRaises(SDKInvalidArgException, e[0], Client(), '')
	def testEntitiesInstanceEmptyData(self):
		for e in self._entityColllection:
			self.assertRaises(SDKInvalidArgException, e[0], Client(), {})



	def testEntitiesHaveSecondaries(self):
		for e in self._entityColllection:
			if not 0 <= 1 < len(e):
				continue

			for sk in e[1]:
				self.assertIsInstance(getattr(e[0](Client(), {'id': 1}), sk), e[1][sk])



if __name__ == '__main__':
	unittest.main()
