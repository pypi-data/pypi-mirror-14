from Exception.BaseException.SDKException import SDKException

class SDKBadJSONResponseException(SDKException):

	_baseMessage = 'JSON remote response is inconsistent or invalid'

	def __init__(self, message = None):
		if message is None:
			message = self._baseMessage
		else:
			message = self._baseMessage + ' - ' + message

		super().__init__(message)
