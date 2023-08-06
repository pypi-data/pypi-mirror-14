import sys
import os

import unittest2 as unittest

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../leantesting'))

from Client import Client

from Exception.SDKInvalidArgException import SDKInvalidArgException

from BaseClass.Entity import Entity
from BaseClass.EntityHandler import EntityHandler

class BaseClassesTest(unittest.TestCase):

	# Entity
	def testEntityDefined(self):
		Entity

	def testEntityDataParsing(self):
		data = {'id': 1}
		entity = Entity(Client(), data)
		self.assertIs(entity.data, data)

	def testEntityInstanceNonArrData(self):
		self.assertRaises(SDKInvalidArgException, Entity, Client(), '')
	def testEntityInstanceEmptyData(self):
		self.assertRaises(SDKInvalidArgException, Entity, Client(), {})
	# END Entity



	# EntityHandler
	def testEntityHandlerDefined(self):
		EntityHandler

	def testEntityHandlerCreateNonArrFields(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.create, '')
	def testEntityHandlerCreateEmptyFields(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.create, {})

	def testEntityHandlerAllNonArrFilters(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.all, '')
	def testEntityHandlerAllInvalidFilters(self):
		h = EntityHandler(Client())
		self.assertRaisesRegex(SDKInvalidArgException, 'XXXfilterXXX', h.all, {'XXXfilterXXX': 9999})
	def testEntityHandlerAllSupportedFilters(self):
		EntityHandler(Client()).all({'include': ''})
		EntityHandler(Client()).all({'limit': 10})
		EntityHandler(Client()).all({'page': 2})

	def testEntityHandlerFindNonIntID(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.find, '')

	def testEntityHandlerDeleteNonIntID(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.delete, '')

	def testEntityHandlerUpdateNonIntID(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.update, '', {'x': 5})
	def testEntityHandlerUpdateNonArrFields(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.update, 5, '')
	def testEntityHandlerUpdateEmptyFields(self):
		h = EntityHandler(Client())
		self.assertRaises(SDKInvalidArgException, h.update, 5, {})
	# END EntityHandler


if __name__ == '__main__':
	unittest.main()
