"""
models.py

"""

from google.appengine.ext import ndb

class Resource(ndb.Model):
	"""Resource: ..."""
	author = ndb.UserProperty()

	name = ndb.StringProperty()
	tags = ndb.StringProperty(repeated = True)
	#pubDate = ndb.DateTimeProperty(auto_now_add=True)
	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	modDate = ndb.DateTimeProperty(auto_now=True)

	date = ndb.DateProperty(auto_now_add=False)
	startTime = ndb.DateTimeProperty(auto_now_add=False)
	endTime = ndb.DateTimeProperty(auto_now_add=False)

	description = ndb.TextProperty(indexed=False)
	duration = ndb.IntegerProperty(indexed=False)
	numReservations = ndb.IntegerProperty(indexed=False)
	maxReservations = ndb.IntegerProperty(indexed=False)
	numsAvailable = ndb.IntegerProperty(indexed=False)
	#
	# user = ndb.StructuredProperty(User)
	#
	# date = ndb.DateProperty()
	# startTime = ndb.TimeProperty(auto_now_add=False)
	# endTime = ndb.TimeProperty(auto_now_add=False)
	# city = ndb.StringProperty()
	#
	# description = ndb.StringProperty()
	#
    #
	#
    #
	# numReservations = ndb.IntegerProperty(indexed=False)
	# maxReservations = ndb.IntegerProperty(indexed=False)


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
	startTime = ndb.DateTimeProperty()
	endTime = ndb.DateTimeProperty()
	numsOfAttendee = ndb.IntegerProperty(indexed=False)

	duration = ndb.IntegerProperty(indexed=False)
