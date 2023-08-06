from Exception.BaseException.SDKException import SDKException

class SDKDuplicateRequestException(SDKException):

	_baseMessage = 'Duplicate request data'

	def __init__(self, message = None):
		if isinstance(message, list):
			message = ', '.join(['`' + el + '`' for el in message])

		if message is None:
			message = self._baseMessage
		else:
			message = self._baseMessage + ' - multiple ' + message

		super().__init__(message)
