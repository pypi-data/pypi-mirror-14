import json
import pycurl
import urllib.parse

try:
	from io import BytesIO
except ImportError:
	from StringIO import StringIO as BytesIO

from Exception.SDKInvalidArgException			import SDKInvalidArgException
from Exception.SDKErrorResponseException		import SDKErrorResponseException
from Exception.SDKBadJSONResponseException		import SDKBadJSONResponseException
from Exception.SDKUnexpectedResponseException	import SDKUnexpectedResponseException

class APIRequest:
	"""

	Represents an API Request definition.

	An APIRequest's parameters can be modified on demand and can be executed multiple times for the same instance.

	"""

	_default_opts = {								# Basic support for extended opts
		'base_uri'	:'https://api.leantesting.com',	# assumed default for API base
		'form_data'	: False,						# sets content type to multipart/form-data if true
		'params'	: {}							# params to be pased in request
	}

	_origin   = None
	_endpoint = None
	_method   = None
	_opts     = None

	def __init__(self, origin, endpoint, method, opts = None):
		"""

		Constructs API request definition.

		Keyword arguments:
		self     APIRequest -- Self instance
		origin   Client   -- Originating client reference
		endpoint str        -- API endpoint
		method   str        -- Method for cURL call - supports GET, POST, PUT or DELETE only
		opts     dict       -- (optional) Additional options to pass to request.
								Request parameters (if any) must bep assed here.

		Exceptions:
		SDKInvalidArgException if method is non-string.
		SDKInvalidArgException if unsupported method is provided.
		SDKInvalidArgException if endpoint is non-string.
		SDKInvalidArgException if opts param is not a dictionary.

		"""

		if opts is None:
			opts = {}

		if not isinstance(method, str):
			raise SDKInvalidArgException('`method` must be a string')
		elif not method in ['GET', 'POST', 'PUT', 'DELETE']:
			raise SDKInvalidArgException('unsupported ' + method + ' `method`')
		elif not isinstance(endpoint, str):
			raise SDKInvalidArgException('`endpoint` must be a string')
		elif not isinstance(opts, dict):
			raise SDKInvalidArgException('`opts` must be a dictionary')

		self._opts = self._default_opts.copy()
		self.updateOpts(opts)

		self._origin   = origin
		self._endpoint = endpoint
		self._method   = method

	def updateOpts(self, opts = None):
		"""

		Updates options list inside API request definition.

		Keyword arguments:
		self     APIRequest -- Self instance
		opts     dict       -- (optional) Additional options array to merge with previous option values

		Exceptions:
		SDKInvalidArgException if opts param is not a dictionary.
		SDKInvalidArgException if provided parameter list is non-dict parameter.

		"""

		if opts is None:
			opts = {}

		if not isinstance(opts, dict):
			raise SDKInvalidArgException('`opts` must be a dictionary')
		elif 'params' in opts and not isinstance(opts['params'], dict):
			raise SDKInvalidArgException('`opts[\'params\']` must be a dictionary')

		self._opts.update(opts)

	def call(self):
		"""

		Executes cURL call as per current API definition state.

		Keyword arguments:
		self APIRequest -- Self instance

		Returns:
		str -- Returns resulting data response from server (including errors and inconsistencies)

		"""

		ch = pycurl.Curl()

		curlHeaders = []

		callUrl = self._opts['base_uri'] + self._endpoint

		ch.setopt(ch.CUSTOMREQUEST, self._method)

		if self._method == 'GET':

			callUrl += '?' + urllib.parse.urlencode(self._opts['params'])

		elif self._method == 'POST' or self._method == 'PUT':

			if self._opts['form_data'] == True and 'file_path' in self._opts.keys():
				ch.setopt(ch.HTTPPOST, [('file', (ch.FORM_FILE, self._opts['file_path'],)),])

				curlHeaders.append('Content-Type: multipart/form-data')
			else:
				jsonData = json.dumps(self._opts['params'])
				ch.setopt(ch.POSTFIELDS, jsonData)

				curlHeaders.append('Content-Type: application/json')
				curlHeaders.append('Content-Length: ' + str(len(jsonData)))

		if isinstance(self._origin.getCurrentToken(), str):
			curlHeaders.append('Authorization: Bearer ' + self._origin.getCurrentToken())

		ch.setopt(ch.HTTPHEADER, curlHeaders)
		ch.setopt(ch.URL, callUrl)

		ch.setopt(ch.HEADER, False)

		curlBuffer = BytesIO()
		ch.setopt(ch.WRITEFUNCTION, curlBuffer.write)
		ch.perform()

		curlData = curlBuffer.getvalue()
		curlData = curlData.decode()

		curlStatus = ch.getinfo(ch.HTTP_CODE)

		ch.close()
		ch = None

		return {
			'data': curlData,
			'status': curlStatus
		}

	def exec_(self):
		"""

		Does cURL data interpretation

		Keyword arguments:
		self APIRequest -- Self instance

		Exceptions:
		SDKErrorResponseException   if the remote response is an error.
			A server response is interpreted as an error if obtained status code differs from expected status code.
			Expected status codes are `200 OK` for GET/POST/PUT, `204 No Content` for DELETE.
		SDKBadJSONResponseException if the remote response contains erronated or invalid JSON contents

		Returns:
		dict    -- In case of successful request, a JSON decoded object is returned.
		boolean -- If a DELETE request is issued, returns true if call is successful (exception otherwise).

		"""

		if not self._origin.debugReturn is None and \
		'data' in self._origin.debugReturn.keys() and \
		'status' in self._origin.debugReturn.keys():

			curlData = self._origin.debugReturn['data']
			curlStatus = self._origin.debugReturn['status']

		else:
			call = self.call()
			curlData = call['data']
			curlStatus = call['status']

		if self._method == 'DELETE':
			expectedHTTPStatus = 204
		else:
			expectedHTTPStatus = 200

		if curlStatus != expectedHTTPStatus:
				raise SDKErrorResponseException(str(curlStatus) + ' - ' + curlData)

		if self._method == 'DELETE':		# if DELETE request, expect no output
			return True

		try:
			jsonData = json.loads(curlData)	# normally, expect JSON qualified output
		except ValueError:
			raise SDKBadJSONResponseException(curlData)

		if not len(jsonData):
			raise SDKUnexpectedResponseException('Empty object received')

		return jsonData
