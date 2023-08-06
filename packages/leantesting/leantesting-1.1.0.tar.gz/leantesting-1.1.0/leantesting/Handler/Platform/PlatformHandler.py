from BaseClass.EntityHandler import EntityHandler

from Handler.Platform.PlatformTypesHandler		import PlatformTypesHandler
from Handler.Platform.PlatformDevicesHandler	import PlatformDevicesHandler
from Handler.Platform.PlatformOSHandler			import PlatformOSHandler
from Handler.Platform.PlatformBrowsersHandler	import PlatformBrowsersHandler

class PlatformHandler(EntityHandler):

	types		= None
	devices		= None
	os			= None
	browsers	= None

	def __init__(self, origin):
		super().__init__(origin)

		self.types		= PlatformTypesHandler(origin)
		self.devices	= PlatformDevicesHandler(origin)
		self.os			= PlatformOSHandler(origin)
		self.browsers	= PlatformBrowsersHandler(origin)
