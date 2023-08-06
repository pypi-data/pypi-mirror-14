from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Platform.PlatformDevice import PlatformDevice

class PlatformDevicesHandler(EntityHandler):

	def find(self, id_):
		super().find(id_)

		req = APIRequest(self._origin, '/v1/platform/devices/' + str(id_), 'GET')
		return PlatformDevice(self._origin, req.exec_())
