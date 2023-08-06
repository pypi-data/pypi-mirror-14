import urllib.parse

from Exception.SDKInvalidArgException import SDKInvalidArgException

from BaseClass.APIRequest import APIRequest

class OAuth2Handler:
	"""

	Handler to manage general authentication routines

	leantesting.com/en/api-docs#oauth-flow

	"""

	_origin = None # Reference to originating Client instance

	def __init__(self, origin):
		"""

		Constructs an OAuth2Handler instance

		Keyword arguments:
		self   OAuth2Handler -- Self instance
		origin Client      -- Originating client reference

		"""

		self._origin = origin

	def generateAuthLink(self, clientID, redirectURI, scope = 'read', state = None):
		"""

		Function that generates link for user to follow in order to request authorization code

		Keyword arguments:
		self        OAuth2Handler -- Self instance
		clientID    str           -- client ID given at application registration
		redirectURI str           -- URL to be redirected to after authorization
		scope       str           -- (optional) comma-separated list of requested scopes (default: 'read')
		state       str           -- (optional) random string for MITM attack prevention

		Exceptions:
		SDKInvalidArgException if provided clientID param is not a string
		SDKInvalidArgException if provided redirectURI param is not a string
		SDKInvalidArgException if provided scope param is not a string
		SDKInvalidArgException if provided state param is not a string

		Returns:
		str - returns URL to follow for authorization code request

		"""

		if not isinstance(clientID, str):
			raise SDKInvalidArgException('`clientID` must be a string')
		elif not isinstance(redirectURI, str):
			raise SDKInvalidArgException('`redirectURI` must be a string')
		elif not isinstance(scope, str):
			raise SDKInvalidArgException('`scope` must be a string')
		elif not state is None and not isinstance(state, str):
			raise SDKInvalidArgException('`state` must be a string')

		baseURL = 'https://leantesting.com/login/oauth/authorize'

		params = {
			'client_id'		: clientID,
			'redirect_uri'	: redirectURI,
			'scope'			: scope
		}

		if not state is None:
			params['state'] = state

		baseURL += '?' + urllib.parse.urlencode(params)
		return baseURL

	def exchangeAuthCode(self, clientID, clientSecret, grantType, code, redirectURI):
		"""

		Generates an access token string from the provided authorization code

		Keyword arguments:
		self         OAuth2Handler -- Self instance
		clientID     str           -- client ID given at application registration
		clientSecret str           -- client secret given at application registration
		grantType    str           -- oauth specific grant_type value (i.e.: authorization_code)
		code         str           -- authorization code obtained from the generated auth link
		redirectURI  str           -- URL to be redirected to after authorization

		Exceptions:
		SDKInvalidArgException if provided clientID param is not a string
		SDKInvalidArgException if provided clientSecret param is not a string
		SDKInvalidArgException if provided grantType param is not a string
		SDKInvalidArgException if provided code param is not a string
		SDKInvalidArgException if provided redirectURI param is not a string

		Returns:
		str - returns obtained access token string

		"""

		if not isinstance(clientID, str):
			raise SDKInvalidArgException('`clientID` must be a string')
		elif not isinstance(clientSecret, str):
			raise SDKInvalidArgException('`clientSecret` must be a string')
		elif not isinstance(grantType, str):
			raise SDKInvalidArgException('`grantType` must be a string')
		elif not isinstance(code, str):
			raise SDKInvalidArgException('`code` must be a string')
		elif not isinstance(redirectURI, str):
			raise SDKInvalidArgException('`redirectURI` must be a string')

		params = {
			'grant_type'	: grantType,
			'client_id'		: clientID,
			'client_secret'	: clientSecret,
			'redirect_uri'	: redirectURI,
			'code'			: code
		}

		req = APIRequest(
			self._origin,
			'/login/oauth/access_token',
			'POST',
			{
				'base_uri'	: 'https://leantesting.com',
				'params'	: params
			}
		)

		resp = req.exec_()
		return resp['access_token']
