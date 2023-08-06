import sys
import os

import unittest2 as unittest

# adds current SDK path to sys.path for imports
sys.path.insert(0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../leantesting'))

from Client import Client

from Exception.SDKInvalidArgException import SDKInvalidArgException

from Handler.Auth.OAuth2Handler	import OAuth2Handler

class OAuth2HandlerTest(unittest.TestCase):

	def testOAuth2HandlerDefined(self):
		OAuth2Handler




	def testOAuth2HandlerGenerateNonStrClientID(self):
		h = OAuth2Handler(Client())
		self.assertRaises(SDKInvalidArgException, h.generateAuthLink, 1, '', '')
	def testOAuth2HandlerGenerateNonStrRedirectURI(self):
		h = OAuth2Handler(Client())
		self.assertRaises(SDKInvalidArgException, h.generateAuthLink, '', 1, '')
	def testOAuth2HandlerGenerateNonStrScope(self):
		h = OAuth2Handler(Client())
		self.assertRaises(SDKInvalidArgException, h.generateAuthLink, '', '', 1)
	def testOAuth2HandlerGenerateNonStrState(self):
		h = OAuth2Handler(Client())
		self.assertRaises(SDKInvalidArgException, h.generateAuthLink, '', '', '', 1)




	def testOAuth2HandlerExchangeNonStrClientID(self):
		client = Client()
		client.debugReturn = '{}'
		h = OAuth2Handler(client)
		self.assertRaises(SDKInvalidArgException, h.exchangeAuthCode, 1, '', '', '', '')
	def testOAuth2HandlerExchangeNonStrClientSecret(self):
		client = Client()
		client.debugReturn = '{}'
		h = OAuth2Handler(client)
		self.assertRaises(SDKInvalidArgException, h.exchangeAuthCode, '', 1, '', '', '')
	def testOAuth2HandlerExchangeNonStrGrantType(self):
		client = Client()
		client.debugReturn = '{}'
		h = OAuth2Handler(client)
		self.assertRaises(SDKInvalidArgException, h.exchangeAuthCode, '', '', 1, '', '')
	def testOAuth2HandlerExchangeNonStrCode(self):
		client = Client()
		client.debugReturn = '{}'
		h = OAuth2Handler(client)
		self.assertRaises(SDKInvalidArgException, h.exchangeAuthCode, '', '', '', 1, '')
	def testOAuth2HandlerExchangeNonStrRedirectURI(self):
		client = Client()
		client.debugReturn = '{}'
		h = OAuth2Handler(client)
		self.assertRaises(SDKInvalidArgException, h.exchangeAuthCode, '', '', '', '', 1)


if __name__ == '__main__':
	unittest.main()
