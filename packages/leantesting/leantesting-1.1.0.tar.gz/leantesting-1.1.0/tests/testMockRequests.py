import sys
import os
import json
import random

import unittest2 as unittest

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../leantesting'))

from Client import Client

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

class MockRequestsTest(unittest.TestCase):

	_client = None

	def setUp(self):
		self._client = Client()

	def _rint(self, min = 100, max = 9999999):
		return random.randint(min, max)
	def _rstr(self, ln = None):
		if ln is None:
			ln = self._rint(1, 15)

		c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
		s = ''

		for i in range(0, ln):
			s += c[random.randint(0, len(c)) - 1]

		return s
	def _robj(self, fields):
		obj = {}
		for f in fields:
			if f[0] == '_':
				obj[f[1:]] = self._rint()
			else:
				obj[f] = self._rstr()
		return obj
	def _rcol(self, name, fields):
		col = {}
		col[name] = []

		for i in range(0, self._rint(1, 7)):
			col[name].append(self._robj(fields))

		totalPages = self._rint(2, 15)
		count = len(col[name])
		perPage = count
		total = totalPages * perPage

		col['meta'] = {
			'pagination': {
				'total': total,
				'count': count,
				'per_page': perPage,
				'current_page': self._rint(1, totalPages),
				'total_pages': totalPages,
				'links': {}
			}
		}

		return col




	# USER
	def testGetUserInformation(self):
		resp = self._robj(['first_name', 'created_at', '_id', 'last_name', 'avatar', 'email', 'username'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		data = self._client.user.getInformation()

		self.assertEqual(resp, data)
	def testGetUserOrganizations(self):
		colName = 'organizations'
		retClass = UserOrganization
		resp = self._rcol(colName, ['_id', 'name', 'alias', 'url', 'logo'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = self._client.user.organizations.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	# END USER






	# PROJECT
	def testListAllProjects(self):
		colName = 'projects'
		retClass = Project
		resp = self._rcol(colName, ['_id', 'name', '_owner_id', '_organization_id', '_is_archived', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = self._client.projects.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testCreateNewProject(self):
		retClass = Project
		resp = self._robj(['_id', 'name', '_owner_id', '_organization_id', '_is_archived', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.projects.create({
			'name': '', 'organization_id': 0
		})

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testRetrieveExistingProject(self):
		retClass = Project
		resp = self._robj(['_id', 'name', '_owner_id', '_organization_id', '_is_archived', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.projects.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)


	def testListProjectSections(self):
		colName = 'sections'
		retClass = ProjectSection
		resp = self._rcol(colName, ['_id', 'name', '_project_id'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).sections.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testAddProjectSection(self):
		retClass = ProjectSection
		resp = self._robj(['_id', 'name', '_project_id'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = Project(self._client, {'id': 0}).sections.create({
			'name': ''
		})

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)


	def testListProjectVersions(self):
		colName = 'versions'
		retClass = ProjectVersion
		resp = self._rcol(colName, ['_id', 'number', '_project_id'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).versions.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testAddProjectVersion(self):
		retClass = ProjectVersion
		resp = self._robj(['_id', 'number', '_project_id'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = Project(self._client, {'id': 0}).versions.create({
			'number': ''
		})

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)


	def testListProjectUsers(self):
		colName = 'users'
		retClass = ProjectUser
		resp = self._rcol(colName, ['_id', 'username', 'first_name', 'last_name', 'avatar', 'email', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).users.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())


	def testListProjectBugTypeScheme(self):
		colName = 'scheme'
		retClass = ProjectBugScheme
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).bugTypeScheme.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testListProjectBugStatusScheme(self):
		colName = 'scheme'
		retClass = ProjectBugScheme
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).bugStatusScheme.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testListProjectBugSeverityScheme(self):
		colName = 'scheme'
		retClass = ProjectBugScheme
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).bugSeverityScheme.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testListProjectBugReproducibilityScheme(self):
		colName = 'scheme'
		retClass = ProjectBugScheme
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).bugReproducibilityScheme.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testListProjectBugPriorityScheme(self):
		colName = 'scheme'
		retClass = ProjectBugScheme
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).bugPriorityScheme.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	# END PROJECT








	# BUG
	def testListBugsInProject(self):
		colName = 'bugs'
		retClass = Bug
		resp = self._rcol(colName, ['_id', 'title', '_status_id', '_severity_id', '_project_version_id',
			'_project_section_id', '_type_id', '_reproducibility_id', '_priority_id', '_assigned_user_id', 'description',
			'expected_results'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Project(self._client, {'id': 0}).bugs.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testCreateNewBug(self):
		retClass = Bug
		resp = self._robj(['_id', 'title', '_status_id', '_severity_id', '_project_version_id',
			'_project_section_id', '_type_id', '_reproducibility_id', '_priority_id', '_assigned_user_id', 'description',
			'expected_results'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = Project(self._client, {'id': 0}).bugs.create({
			'title': '', 'status_id': 0, 'severity_id': 0, 'project_version_id': 0, 'project_section_id': 0,
			'type_id': 0, 'reproducibility_id': 0, 'priority_id': 0, 'assigned_user_id': 0, 'description': '',
			'expected_results': ''
		})

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testRetrieveExistingBug(self):
		retClass = Bug
		resp = self._robj(['_id', 'title', '_status_id', '_severity_id', '_project_version_id',
			'_project_section_id', '_type_id', '_reproducibility_id', '_priority_id', '_assigned_user_id', 'description',
			'expected_results'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.bugs.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testUpdateBug(self):
		retClass = Bug
		resp = self._robj(['_id', 'title', '_status_id', '_severity_id', '_project_version_id',
			'_project_section_id', '_type_id', '_reproducibility_id', '_priority_id', '_assigned_user_id', 'description',
			'expected_results'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.bugs.update(0, {
			'title': '', 'status_id': 0, 'severity_id': 0, 'project_version_id': 0, 'project_section_id': 0,
			'type_id': 0, 'assigned_user_id': 0, 'description': '', 'expected_results': '', 'priority_id': 0
		})

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testDeleteBug(self):
		self._client.debugReturn = {'data': None, 'status': 204}

		data = self._client.bugs.delete(0)

		self.assertTrue(data)
	# END BUG







	# BUG COMMENTS
	def testListBugComments(self):
		colName = 'comments'
		retClass = BugComment
		resp = self._rcol(colName, ['_id', 'text', '_owner_id', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Bug(self._client, {'id': 0}).comments.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	# END BUG COMMENTS








	# BUG ATTACHMENTS
	def testListBugAttachments(self):
		colName = 'attachments'
		retClass = BugAttachment
		resp = self._rcol(colName, ['_id', '_owner_id', 'url', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = Bug(self._client, {'id': 0}).attachments.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testCreateNewAttachment(self):
		retClass = BugAttachment
		resp = self._robj(['_id', '_owner_id', 'url', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		_fp = os.path.dirname(os.path.realpath(__file__)) + '/res/upload_sample.jpg'
		obj = Bug(self._client, {'id': 0}).attachments.upload(_fp)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testRetrieveExistingAttachment(self):
		retClass = BugAttachment
		resp = self._robj(['_id', '_owner_id', 'url', 'created_at'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.attachments.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testDeleteAttachment(self):
		self._client.debugReturn = {'data': None, 'status': 204}

		data = self._client.attachments.delete(0)

		self.assertTrue(data)
	# END BUG ATTACHMENTS








	# PLATFORM
	def testListPlatformTypes(self):
		colName = 'types'
		retClass = PlatformType
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = self._client.platform.types.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testRetrievePlatformType(self):
		retClass = PlatformType
		resp = self._robj(['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.platform.types.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)

	def testListPlatformDevices(self):
		colName = 'devices'
		retClass = PlatformDevice
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = PlatformType(self._client, {'id': 0}).devices.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testRetrievePlatformDevice(self):
		retClass = PlatformDevice
		resp = self._robj(['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.platform.devices.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)

	def testListOS(self):
		colName = 'os'
		retClass = PlatformOS
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = self._client.platform.os.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testRetrieveOS(self):
		retClass = PlatformOS
		resp = self._robj(['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.platform.os.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testListOSVersions(self):
		colName = 'versions'
		retClass = PlatformOSVersion
		resp = self._rcol(colName, ['_id', 'number'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = PlatformOS(self._client, {'id': 0}).versions.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())

	def testListBrowsers(self):
		colName = 'browsers'
		retClass = PlatformBrowser
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = self._client.platform.browsers.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	def testRetrieveBrowser(self):
		retClass = PlatformBrowser
		resp = self._robj(['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		obj = self._client.platform.browsers.find(0)

		self.assertEqual(resp, obj.data)
		self.assertIsInstance(obj, retClass)
	def testListBrowserVersions(self):
		colName = 'versions'
		retClass = PlatformBrowserVersion
		resp = self._rcol(colName, ['_id', 'name'])
		self._client.debugReturn = {'data': json.dumps(resp), 'status': 200}

		col = PlatformBrowser(self._client, {'id': 0}).versions.all()

		self.assertEqual(resp[colName], col.toArray())
		self.assertIsInstance(col._collection[0], retClass)
		self.assertEqual(resp['meta']['pagination']['total'], col.total())
		self.assertEqual(resp['meta']['pagination']['total_pages'], col.totalPages())
		self.assertEqual(resp['meta']['pagination']['count'], col.count())
	# END PLATFORM


if __name__ == '__main__':
	unittest.main()
