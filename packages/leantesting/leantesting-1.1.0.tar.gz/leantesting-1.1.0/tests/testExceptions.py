import sys
import os

import unittest2 as unittest

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../leantesting'))

from Exception.BaseException.SDKException import SDKException

from Exception.SDKBadJSONResponseException		import SDKBadJSONResponseException
from Exception.SDKDuplicateRequestException		import SDKDuplicateRequestException
from Exception.SDKErrorResponseException		import SDKErrorResponseException
from Exception.SDKIncompleteRequestException	import SDKIncompleteRequestException
from Exception.SDKInvalidArgException			import SDKInvalidArgException
from Exception.SDKMissingArgException			import SDKMissingArgException
from Exception.SDKUnexpectedResponseException	import SDKUnexpectedResponseException
from Exception.SDKUnsupportedRequestException	import SDKUnsupportedRequestException


class ExceptionsTest(unittest.TestCase):

	_exceptionCollection = [
		[SDKException],
		[SDKBadJSONResponseException],
		[SDKDuplicateRequestException],
		[SDKErrorResponseException],
		[SDKIncompleteRequestException],
		[SDKInvalidArgException],
		[SDKMissingArgException],
		[SDKUnexpectedResponseException],
		[SDKUnsupportedRequestException]
	]

	def testExceptionsDefined(self):
		for e in self._exceptionCollection:
			e[0]



	def testExceptionsRaiseNoArgs(self):
		for e in self._exceptionCollection:
			try:
				raise e[0]
			except Exception as ex:
				if not ex.__class__.__name__ == e[0].__name__:
					self.fail('Unexpected exception received. Expected ' + e[0].__name__)
				if not 'SDK Error' in ex.message:
					self.fail('Unexpected exception message for ' + e[0].__name__)
	def testExceptionsRaiseWithStr(self):
		for e in self._exceptionCollection:
			try:
				raise e[0]('XXXmsgXXX')
			except Exception as ex:
				if not ex.__class__.__name__ == e[0].__name__:
					self.fail('Unexpected exception received. Expected ' + e[0].__name__)
				if not 'XXXmsgXXX' in ex.message:
					self.fail('Unexpected exception message for ' + e[0].__name__)



	# RAISE WITH ARR (when supported)
	def testDuplicateRequestRaiseWithArr(self):
		try:
			raise SDKDuplicateRequestException(['xx', 'yy', 'zz'])
		except SDKDuplicateRequestException as ex:
			if not 'Duplicate' in ex.message:
				self.fail('Unexpected exception message')
		except:
			self.fail('Unexpected exception received')
	def testIncompleteRequestRaiseWithArr(self):
		try:
			raise SDKIncompleteRequestException(['xx', 'yy', 'zz'])
		except SDKIncompleteRequestException as ex:
			if not 'Incomplete' in ex.message:
				self.fail('Unexpected exception message')
		except:
			self.fail('Unexpected exception received')
	def testUnsupportedRequestRaiseWithArr(self):
		try:
			raise SDKUnsupportedRequestException(['xx', 'yy', 'zz'])
		except SDKUnsupportedRequestException as ex:
			if not 'Unsupported' in ex.message:
				self.fail('Unexpected exception message')
		except:
			self.fail('Unexpected exception received')
	# END RAISE WITH ARR

if __name__ == '__main__':
	unittest.main()
