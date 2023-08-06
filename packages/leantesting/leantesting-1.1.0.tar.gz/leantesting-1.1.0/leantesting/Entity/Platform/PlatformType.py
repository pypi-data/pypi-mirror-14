from BaseClass.Entity import Entity

from Handler.Platform.PlatformTypeDevicesHandler import PlatformTypeDevicesHandler

class PlatformType(Entity):

	devices = None

	def __init__(self, origin, data):
		super().__init__(origin, data)

		self.devices = PlatformTypeDevicesHandler(origin, data['id'])
