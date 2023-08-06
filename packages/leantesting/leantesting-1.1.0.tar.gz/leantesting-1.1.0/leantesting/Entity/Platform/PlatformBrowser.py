from BaseClass.Entity import Entity

from Handler.Platform.PlatformBrowserVersionsHandler import PlatformBrowserVersionsHandler

class PlatformBrowser(Entity):

	versions = None

	def __init__(self, origin, data):
		super().__init__(origin, data)

		self.versions = PlatformBrowserVersionsHandler(origin, data['id'])
