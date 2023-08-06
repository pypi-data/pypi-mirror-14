class SDKException(Exception):

	def __init__(self, message = None):
		super().__init__(message)

		if message is None:
			message = 'Unknown SDK Error'
		else:
			message = 'SDK Error: ' + message

		self.message = message

	def __str__(self):
		return repr(self.message)
