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
	startTime = ndb.TimeProperty(auto_now_add=False)
	endTime = ndb.TimeProperty(auto_now_add=False)

	description = ndb.StringProperty()
	duration = ndb.IntegerProperty(indexed=False)
	numReservations = ndb.IntegerProperty(indexed=False)
	maxReservations = ndb.IntegerProperty(indexed=False)
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



class Reservation(ndb.Model):
	"""Resource: ..."""
	author = ndb.UserProperty()


	name = ndb.StringProperty()

	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	modDate = ndb.DateTimeProperty(auto_now=True)

	date = ndb.DateProperty()
	startTime = ndb.TimeProperty()
	endTime = ndb.TimeProperty()

	duration = ndb.IntegerProperty(indexed=False)
