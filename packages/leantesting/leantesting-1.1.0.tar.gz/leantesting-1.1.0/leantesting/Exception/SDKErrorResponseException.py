from Exception.BaseException.SDKException import SDKException

class SDKErrorResponseException(SDKException):

	def __init__(self, message = None):
		if message is None:
			message = 'Unknown remote error'
		else:
			message = 'Got error response: ' + message

		super().__init__(message)
