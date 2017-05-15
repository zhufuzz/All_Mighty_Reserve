"""
models.py

"""

from google.appengine.ext import ndb

class User(ndb.Model):
	"""User: the person..."""
	identity=ndb.StringProperty(indexed=False)
	email=ndb.StringProperty(indexed=False)


class Resource(ndb.Model):
	"""Resource: ..."""
	uuid = ndb.StringProperty()
	resourceName = ndb.StringProperty()
	startTime = ndb.DateTimeProperty(auto_now_add=False)
	endTime = ndb.DateTimeProperty(auto_now_add=False)
	user = ndb.StructuredProperty(User)
	date = ndb.DateTimeProperty(auto_now_add=False)
	tags = ndb.StringProperty(repeated=True)
	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	numReservations = ndb.IntegerProperty(indexed=False)


class Reservation(ndb.Model):
	"""Resource: ..."""
	user = ndb.StructuredProperty(User)
	uuid = ndb.StringProperty()
	resourceUUID = ndb.StringProperty()
	resourceName = ndb.StringProperty()
	startTime = ndb.DateTimeProperty(auto_now_add=False)
	endTime = ndb.DateTimeProperty(auto_now_add=False)
	duration = ndb.StringProperty(indexed=False)
	pubDate = ndb.DateTimeProperty(auto_now_add=True)
