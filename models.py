"""
models.py

"""
from google.appengine.ext import ndb

class Resource(ndb.Model):
	"""Resource: ..."""
	author = ndb.UserProperty()

	name = ndb.StringProperty()
	tags = ndb.StringProperty(repeated = True)
	description = ndb.TextProperty(indexed=False)

	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	modDate = ndb.DateTimeProperty(auto_now=True)
	lastReserveDate = ndb.DateTimeProperty()

	startDateTime = ndb.DateTimeProperty(auto_now_add=False)
	endDateTime = ndb.DateTimeProperty(auto_now_add=False)
	duration = ndb.StringProperty(indexed=False)

	numReservations = ndb.IntegerProperty(indexed=False)
	maxReservations = ndb.IntegerProperty(indexed=False)
	numsAvailable = ndb.IntegerProperty(indexed=False)

	# @classmethod
	# def query_resource(cls, ancestor_key):
	# 	return cls.query(ancestor=ancestor_key).order(-cls.date)


class Reservation(ndb.Model):
	"""Resource: ..."""
	author = ndb.UserProperty()

	name = ndb.StringProperty()

	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	modDate = ndb.DateTimeProperty(auto_now=True)

	date = ndb.DateProperty()
	startDateTime = ndb.DateTimeProperty()
	endDateTime = ndb.DateTimeProperty()
	duration = ndb.StringProperty(indexed=False)

	numsOfAttendee = ndb.IntegerProperty(indexed=False)


