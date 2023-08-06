from BaseClass.Entity import Entity

from Handler.Platform.PlatformOSVersionsHandler import PlatformOSVersionsHandler

class PlatformOS(Entity):

	versions = None

	def __init__(self, origin, data):
		super().__init__(origin, data)

		self.versions = PlatformOSVersionsHandler(origin, data['id'])
