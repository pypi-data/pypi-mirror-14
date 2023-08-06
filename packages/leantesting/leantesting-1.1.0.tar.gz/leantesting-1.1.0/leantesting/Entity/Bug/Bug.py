from BaseClass.Entity import Entity

from Handler.Bug.BugCommentsHandler		import BugCommentsHandler
from Handler.Bug.BugAttachmentsHandler	import BugAttachmentsHandler

class Bug(Entity):

	comments    = None
	attachments = None

	def __init__(self, origin, data):
		super().__init__(origin, data)

		self.comments    = BugCommentsHandler(origin, data['id'])
		self.attachments = BugAttachmentsHandler(origin, data['id'])
