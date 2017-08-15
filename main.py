"""main.py"""
import os
import re
import urllib
import time
import uuid
import jinja2
import webapp2
from time import sleep
from datetime import datetime, time, timedelta, date
from email import utils
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from models import Resource
from models import Reservation
from utils import checkUser

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(
		os.path.join(os.path.dirname(__file__), 'templates')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
DEFAULT_RESOURCE_NAME = 'default_resource_name'

#Route to index page and present user's reservation
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
			# thisResource.numReservations = thisResource.numReservations - thisReservation.numsOfAttendee
			thisResource.numsAvailable = thisResource.maxReservations - thisResource.numReservations
			thisResource.put()
			deleteReservationKey.delete()

		reservations = Reservation.query(user == Reservation.author).order(-Reservation.pubDate)
		reservations = reservations.fetch()

		# nowStr = datetime.now().strftime("%Y-%m-%d - %H:%M")
		# nowDateTime = datetime.strptime(nowStr, "%Y-%m-%d - %H:%M")
		# resource_query = Resource.query(Reservation.)
		# .filter(Reservation.endTime.date() >= date.today())


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

			# ndb.delete_multi(deleteResourceKey)

			deleteResourceKey.delete()

		resource_query = Resource.query().order(-Resource.modDate)
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

		resource_query = Resource.query(user == Resource.author).order(-Resource.modDate)
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

##################################################################

# @ndb.transactional
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
		resource.name = self.request.get('name')
		resource.tags = self.request.get('tags').strip().split(',')
		resource.maxReservations = int(self.request.get('maxReservations'))
		resource.numsAvailable = int(self.request.get('maxReservations'))
		resource.numReservations = 0
		resource.description = self.request.get('description')

		startDateTimeStr = self.request.get('startTime')
		endDateTimeStr = self.request.get('endTime')
		resource.startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		resource.endDateTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')

		resource.duration = (resource.endDateTime - resource.startDateTime).seconds
		resource.put()

		url = '/ResourceContent?resourceID=%s' % resource.key.urlsafe()
		self.redirect(url)

######################################################

# class DeleteResource(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		url, url_linktext = checkUser(user, self)
#
# 		deleteResourceStr = self.request.get('resourceID')
# 		if deleteResourceStr != '':
# 			deleteResourceKey = ndb.Key(urlsafe=deleteResourceStr)
# 			deleteResourceKey.delete()
#
# 		template_values = {
# 			'user': user,
# 			'url': url,
# 			'url_linktext': url_linktext,
# 		}
#
# 		template = JINJA_ENVIRONMENT.get_template('allResources.html')
# 		self.response.write(template.render(template_values))
#
# class DeleteReservation(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		url, url_linktext = checkUser(user, self)
#
# 		deleteReservationStr = self.request.get('reservationID')
# 		if deleteReservationStr != '':
# 			deleteResourceKey = ndb.Key(urlsafe=deleteReservationStr)
# 			deleteResourceKey.delete()
#
# 		template_values = {
# 			'user': user,
# 			'url': url,
# 			'url_linktext': url_linktext,
# 		}
#
# 		template = JINJA_ENVIRONMENT.get_template('index.html')
# 		self.response.write(template.render(template_values))



#def get_url_safe_key(sandy_key):
#     url_string = sandy_key.urlsafe()
#     return url_string
#
#
# def get_entity_from_url_safe_key(url_string):
#     sandy_key = ndb.Key(urlsafe=url_string)
#     sandy = sandy_key.get()
#     return sandy
#
#
# def get_key_and_numeric_id_from_url_safe_key(url_string):
#     key = ndb.Key(urlsafe=url_string)
#     kind_string = key.kind()
#     ident = key.id()
#     return key, ident, kind_string

##########################################################

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
		resource.put()

		reservation.author = users.get_current_user()
		reservation.name = self.request.get('name')
		startDateTimeStr = self.request.get('startDateTime')
		endDateTimeStr = self.request.get('endDateTime')
		reservation.startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		reservation.endStartTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')
		reservation.duration = (reservation.endStartTime - reservation.startDateTime).seconds
		reservation.put()

		# url = '/ResourceContent?resourceID=%s' % resource.key.urlsafe()
		self.redirect('/')

##################################################################


# class ReserveBase(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		url, url_linktext = checkUser(user, self)
#
# 		template_values = {
# 			'user': user,
# 			'url': url,
# 			'url_linktext': url_linktext,
# 		}
# 		template = JINJA_ENVIRONMENT.get_template('reserve.html')
# 		self.response.write(template.render(template_values))



##################################################################


# class Reservations(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		url, url_linktext = checkUser(user, self)
#
# 		resourceIDStr = self.request.get('resourceID')
# 		resource = ndb.Key(urlsafe=resourceIDStr).get()
#
# 		reservations = Reservation.query(ancestor = resource.key).order(-Reservation.pubDate).fetch()
# 		# resource_query = Resource.query(Reservation.)
# 		# .filter(Reservation.endTime.date() >= date.today())
# 		# reservations = reservation_query.fetch()
#
# 		template_values = {
# 			'reservations': reservations,
# 			'user': user,
# 			'url': url,
# 			'url_linktext': url_linktext,
# 			'today': date.today()
# 		}
# 		template = JINJA_ENVIRONMENT.get_template('resource_reservations.html')
# 		self.response.write(template.render(template_values))


##################################################################

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
		resource = Resource()
		resource.author = users.get_current_user()
		resource.name = self.request.get('name')
		resource.tags = self.request.get('tags').strip().split(',')
		resource.maxReservations = int(self.request.get('maxReservations'))
		resource.numsAvailable = int(self.request.get('maxReservations'))
		resource.numReservations = 0
		resource.description = self.request.get('description')

		startDateTimeStr = self.request.get('startDateTime')
		endDateTimeStr = self.request.get('endDateTime')
		resource.startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		resource.endDateTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')
		resource.duration = (resource.endDateTime - resource.startDateTime).seconds
		resource.put()

		url = '/ResourceContent?resourceID=%s' % resource.key.urlsafe()
		self.redirect(url)

#############################

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

		# update the numReservations and numsAvailable of this resource when delete the reservation
		deleteReservationStr = self.request.get('deleteReservationID')
		if deleteReservationStr != '':
			deleteReservationKey = ndb.Key(urlsafe=deleteReservationStr)
			thisReservation = deleteReservationKey.get()
			thisResource = deleteReservationKey.parent().get()
			thisResource.numReservations = thisResource.numReservations - thisReservation.numsOfAttendee
			# thisResource.numReservations = thisResource.numReservations - thisReservation.numsOfAttendee
			thisResource.numsAvailable = thisResource.maxReservations - thisResource.numReservations
			thisResource.put()
			deleteReservationKey.delete()

		resourceID = self.request.get('resourceID')
		resource = ndb.Key(urlsafe=resourceID).get()

		reservations = Reservation.query(ancestor=resource.key).order(-Reservation.pubDate).fetch()

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'resource':resource,
			'reservations':reservations,
			'now': now
		}

		# if self.request.get('resourceID'):
		# 	resourceID = self.request.get('resourceID')
		# 	resource = ndb.Key(urlsafe=resourceID).get()
		# 	template_values['resource'] = resource

		template = JINJA_ENVIRONMENT.get_template('resource_content.html')
		self.response.write(template.render(template_values))

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

##################################################################
# self.redirect('/?' + urllib.urlencode(
# 	{'guestbook_name': guestbook_name}))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/CreateResource', CreateResource),
	('/AllResources', AllResources),
	# ('/DeleteResource', DeleteResource),
	# ('/MyResource', MyResource),
	('/MyResource', MyResource),
	# ('/DeleteReservation', DeleteReservation),
	# ('/ReserveBase', ReserveBase),
    #
	# ('/Reservations', Reservations),
	('/Reserve', Reserve),
	('/EditResource', EditResource),
	('/ResourceContent', ResourceContent),
	('/ResourcesWithTag', ResourcesWithTag),

], debug=True)

