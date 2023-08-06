from Exception.BaseException.SDKException import SDKException

class SDKUnsupportedRequestException(SDKException):

	_baseMessage = 'Unsupported request data'

	def __init__(self, message = None):
		if isinstance(message, list):
			message = ', '.join(['`' + el + '`' for el in message])

		if message is None:
			message = self._baseMessage
		else:
			message = self._baseMessage + ' - invalid ' + message

		super().__init__(message)
