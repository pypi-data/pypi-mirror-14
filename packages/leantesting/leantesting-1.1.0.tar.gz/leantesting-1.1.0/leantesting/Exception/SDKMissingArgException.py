from Exception.BaseException.SDKException import SDKException

class SDKMissingArgException(SDKException):

	_baseMessage = 'Missing argument'

	def __init__(self, message = None):
		if message is None:
			message = self._baseMessage
		else:
			message = self._baseMessage + ' `' + message + '`'

		super().__init__(message)
