# encoding: utf-8
"""
models.py

"""
from google.appengine.ext import ndb

class Resource(ndb.Model):
	"""Resource: ..."""
	author = ndb.UserProperty(indexed=True)

	name = ndb.StringProperty(indexed=True)
	tags = ndb.StringProperty(indexed=True, repeated = True)
	description = ndb.TextProperty(indexed=False)


	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	modDate = ndb.DateTimeProperty(auto_now=True)
	lastReserveDate = ndb.DateTimeProperty(indexed=True)

	startDateTime = ndb.DateTimeProperty(auto_now_add=False)
	endDateTime = ndb.DateTimeProperty(auto_now_add=False)
	duration = ndb.StringProperty(indexed=False)

	numReservations = ndb.IntegerProperty(indexed=False)
	maxReservations = ndb.IntegerProperty(indexed=False)
	# numsAvailable = maxReservations - numReservations
	numsAvailable = ndb.IntegerProperty(indexed=False)

	# image_blob_key = ndb.BlobKeyProperty(indexed=False)
	image = ndb.BlobProperty(indexed=False)

	# @classmethod
	# def query_resource(cls, ancestor_key):
	# 	return cls.query(ancestor=ancestor_key).order(-cls.date)


class Reservation(ndb.Model):
	"""Resource: ..."""
	# User who make reservation of a resource
	author = ndb.UserProperty(indexed=True)
	# Name of the reservation
	name = ndb.StringProperty(indexed=True)

	pubDate = ndb.DateTimeProperty(auto_now_add=True)
	modDate = ndb.DateTimeProperty(auto_now=True)

	# date = ndb.DateProperty()
	startDateTime = ndb.DateTimeProperty()
	endDateTime = ndb.DateTimeProperty()
	duration = ndb.StringProperty(indexed=False)

	numsOfAttendee = ndb.IntegerProperty(indexed=False)


