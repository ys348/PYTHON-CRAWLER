
from google.appengine.ext import ndb


class urlNode(ndb.Model):
	node_name = ndb.StringProperty(required=True)
	node_position = ndb.StringProperty(required=True)
	node_fullUrl = ndb.StringProperty(required=True)
	node_parentId = ndb.StringProperty(required=True)
	node_count = ndb.IntegerProperty(default = 0)