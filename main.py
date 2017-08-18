"""main.py"""
import os
from datetime import datetime
import time
from time import sleep

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from models import Reservation
from models import Resource

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(
		os.path.join(os.path.dirname(__file__), 'templates')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
DEFAULT_RESOURCE_NAME = 'default_resource_name'


#Route to index page and present user's reservations
class MainPage(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		# update the numReservations and numsAvailable of this resource when delete the reservation
		deleteReservationStr = self.request.get('deleteReservationID')
		if deleteReservationStr != '':
			deleteReservationKey = ndb.Key(urlsafe=deleteReservationStr)
			thisReservation = deleteReservationKey.get()
			thisResource = deleteReservationKey.parent().get()
			thisResource.numReservations = thisResource.numReservations - thisReservation.numsOfAttendee
			thisResource.numsAvailable = thisResource.maxReservations - thisResource.numReservations
			thisResource.put()
			deleteReservationKey.delete()
			sleep(0.2)

		# The expired reservations will be deleted from data store before presenting
		deleteExpiredReservationsKeys = Reservation.query(Reservation.endDateTime <= datetime.now()).fetch(keys_only=True)
		for deleteReservationKey in deleteExpiredReservationsKeys:
			thisReservation = deleteReservationKey.get()
			resource = deleteReservationKey.parent().get()
			resource.numReservations = resource.numReservations - thisReservation.numsOfAttendee
			resource.numsAvailable = resource.maxReservations - resource.numReservations
			resource.put()

		ndb.delete_multi(deleteExpiredReservationsKeys)

		#query reservations of the current user, order them based the reservation time('pubDate')
		reservations = Reservation.query(user == Reservation.author).order(-Reservation.pubDate).fetch()

		template_values = {
			'reservations': reservations,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,

			'now': now
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

##################################################################################

#query all resources in the system
class AllResources(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		deleteResourceStr = self.request.get('delResourceID')
		if deleteResourceStr != '':
			deleteResourceKey = ndb.Key(urlsafe=deleteResourceStr)
			deleteReservationKeys = Reservation.query(ancestor = deleteResourceKey).fetch(keys_only=True)
			ndb.delete_multi(deleteReservationKeys)
			deleteResourceKey.delete()

		resource_query = Resource.query().order(-Resource.lastReserveDate)
		resources = resource_query.fetch()

		template_values = {
			'resources': resources,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'now': now
		}

		template = JINJA_ENVIRONMENT.get_template('allResources.html')
		self.response.write(template.render(template_values))

##########################################

#query resources created by the current user
class MyResource(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		resource_query = Resource.query(user == Resource.author).order(-Resource.lastReserveDate)
		resources = resource_query.filter().fetch()

		template_values = {
			'resources': resources,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'now': now
		}
		template = JINJA_ENVIRONMENT.get_template('myResource.html')
		self.response.write(template.render(template_values))

##################################################################################

#create resource
class CreateResource(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'now': now
		}

		template = JINJA_ENVIRONMENT.get_template('createResource.html')
		self.response.write(template.render(template_values))

	def post(self):
		resource = Resource()
		resource.author = users.get_current_user()
		resource.name = self.request.get('name').strip()
		tagList1 = self.request.get('tags').strip().split(',')
		for tag in tagList1:
			if (tag is not None) and (tag.strip() != ""):
				resource.tags.append(tag.strip())
		resource.maxReservations = int(self.request.get('maxReservations'))
		resource.numsAvailable = int(self.request.get('maxReservations'))
		resource.numReservations = 0
		resource.description = self.request.get('description').strip()

		startDateTimeStr = self.request.get('startDateTime')
		endDateTimeStr = self.request.get('endDateTime')
		startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		endDateTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')
		resource.startDateTime = startDateTime
		resource.endDateTime = endDateTime
		duration = str(endDateTime - startDateTime)
		resource.duration = duration

		resource.put()
		sleep(0.2)

		url = '/ResourceContent?resourceID=%s' % resource.key.urlsafe()
		self.redirect(url)

##################################################################################

#Make reservation of a resource.
#DateTime validation is done by the frontend, in the checkInput.js
class Reserve(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		resourceIDStr = self.request.get('resourceID')
		resourceID = ndb.Key(urlsafe=resourceIDStr)
		resource = resourceID.get()
		resource.numsAvailable = resource.maxReservations - resource.numReservations
		resource.put()
		sleep(0.2)

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'resource': resource,
			'now': now
		}

		template = JINJA_ENVIRONMENT.get_template('resource_reserve.html')
		self.response.write(template.render(template_values))

	def post(self):
		resourceID = self.request.get('resourceID')
		resource = ndb.Key(urlsafe = resourceID).get()
		reservation = Reservation(parent = resource.key)
		reservation.author = user = users.get_current_user()
		reservation.numsOfAttendee = int(self.request.get('numsOfAttendee'))
		resource.numsAvailable = resource.numsAvailable - int(self.request.get('numsOfAttendee'))
		resource.numReservations = resource.numReservations + int(self.request.get('numsOfAttendee'))
		#Update the last Reserve Date of this resource
		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')
		resource.lastReserveDate = now
		#Save the resource
		resource.put()

		#Get the reservation info from page
		reservation.author = users.get_current_user()
		reservation.name = self.request.get('name').strip()
		startDateTimeStr = self.request.get('startDateTime')
		endDateTimeStr = self.request.get('endDateTime')
		startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		endDateTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')
		reservation.startDateTime = startDateTime
		reservation.endDateTime = endDateTime
		duration = str(endDateTime - startDateTime)
		reservation.duration = duration
		# Save the reservation
		reservation.put()
		sleep(0.2)

		self.redirect('/')

##################################################################################

#Edit resource. Previous data will be presented.
#DateTime validation is done by the frontend, in the checkInput.js
class EditResource(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		resourceID = self.request.get('resourceID')
		resource = ndb.Key(urlsafe=resourceID).get()

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'resource':resource,
			'now': now
		}

		template = JINJA_ENVIRONMENT.get_template('resource_edit.html')
		self.response.write(template.render(template_values))

	def post(self):
		resourceID = self.request.get('resourceID')
		resource = Resource()
		resource.author = users.get_current_user()
		# Get the resource info from page
		resource.name = self.request.get('name').strip()
		tagList1 = self.request.get('tags').strip().split(',')
		for tag in tagList1:
			if (tag is not None) and (tag.strip() != ""):
				resource.tags.append(tag.strip())

		resource.maxReservations = int(self.request.get('maxReservations'))
		resource.numsAvailable = int(self.request.get('maxReservations'))
		resource.numReservations = 0
		resource.description = self.request.get('description').strip()

		startDateTimeStr = self.request.get('startDateTime')
		endDateTimeStr = self.request.get('endDateTime')
		startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		endDateTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')
		resource.startDateTime = startDateTime
		resource.endDateTime = endDateTime
		duration = str(endDateTime - startDateTime)
		resource.duration = duration
		#update the resource
		resource.put()
		sleep(0.2)

		url = '/ResourceContent?resourceID=%s' % resource.key.urlsafe()
		self.redirect(url)

##################################################################################

# Present content of a resource, and all reservations of this resource(including reservations of other users).
# Delete all expired reservations before presenting the resource content
class ResourceContent(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		# Update the numReservations and numsAvailable of this resource when delete the reservation
		# Only the owner of the reservation will be presented a 'delete' button
		#
		deleteReservationStr = self.request.get('deleteReservationID')
		if deleteReservationStr != '':
			deleteReservationKey = ndb.Key(urlsafe=deleteReservationStr)
			thisReservation = deleteReservationKey.get()
			resource = deleteReservationKey.parent().get()
			resource.numReservations = resource.numReservations - thisReservation.numsOfAttendee
			resource.numsAvailable = resource.maxReservations - resource.numReservations
			resource.put()
			deleteReservationKey.delete()
			# sleep(0.2)
		else:
			resourceID = self.request.get('resourceID')
			resource = ndb.Key(urlsafe=resourceID).get()

		# Delete expired reservations and update the resource of this reservation (numReservations and numsAvailable)
		# Expiration is when the end of reservation is passed, so you can reserve even when the resource has started
		deleteExpiredReservationsKeys = Reservation.query(Reservation.endDateTime <= datetime.now()).fetch(keys_only=True)
		for deleteReservationKey in deleteExpiredReservationsKeys:
			thisReservation = deleteReservationKey.get()
			resource = deleteReservationKey.parent().get()
			resource.numReservations = resource.numReservations - thisReservation.numsOfAttendee
			resource.numsAvailable = resource.maxReservations - resource.numReservations
			resource.put()
		ndb.delete_multi(deleteExpiredReservationsKeys)

		# Query the reservations of this resource
		reservations = Reservation.query(ancestor=resource.key).order(-Reservation.pubDate).fetch()

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'resource':resource,
			'reservations':reservations,
			'now': now
		}

		template = JINJA_ENVIRONMENT.get_template('resource_content.html')
		self.response.write(template.render(template_values))

##################################################################################

class ResourcesWithTag(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			self.redirect(users.create_login_url(self.request.uri))
		user = users.get_current_user()

		nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.strptime(nowStr, '%Y-%m-%d %H:%M:%S')

		tagIDStr = self.request.get('tag')
		resources = Resource.query(tagIDStr == Resource.tags).fetch()

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'resources': resources,
			'now': now
		}

		template = JINJA_ENVIRONMENT.get_template('tag.html')
		self.response.write(template.render(template_values))

##################################################################################

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/CreateResource', CreateResource),
	('/AllResources', AllResources),
	('/MyResource', MyResource),
	('/Reserve', Reserve),
	('/EditResource', EditResource),
	('/ResourceContent', ResourceContent),
	('/ResourcesWithTag', ResourcesWithTag),
], debug=True)

