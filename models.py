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

	author = ndb.UserProperty()

	resourceName = ndb.StringProperty()
	tags = ndb.StringProperty(repeated = True)
	#pubDate = ndb.DateTimeProperty(auto_now_add=True)
	pubDate = ndb.StringProperty()
	date = ndb.StringProperty()
	startTime = ndb.StringProperty()
	endTime = ndb.StringProperty()

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
	user = ndb.StructuredProperty(User)
	uuid = ndb.StringProperty()
	resourceUUID = ndb.StringProperty()
	resourceName = ndb.StringProperty()

	date = ndb.DateProperty()


	startTime = ndb.DateTimeProperty(auto_now_add=False)
	endTime = ndb.DateTimeProperty(auto_now_add=False)
	duration = ndb.StringProperty(indexed=False)

	pubDate = ndb.DateTimeProperty(auto_now_add=True)
