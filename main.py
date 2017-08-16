"""main.py"""
import os
from datetime import datetime
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
			thisResource.numsAvailable = thisResource.maxReservations - thisResource.numReservations
			thisResource.put()
			deleteReservationKey.delete()
			sleep(0.2)


		# resource_query = Resource.query(
		# 	Resource.startDateTime
		# 	>=
		# 	datetime.now()
		# ).order(-Resource.startDateTime).order(-Resource.modDate)


		# reservations = Reservation.query(user == Reservation.author)
		# reservations = reservations.filter(Reservation.startDateTime > datetime.now())
		# reservations = reservations.order(-Reservation.pubDate)
		# reservations = reservations.fetch()

		deleteReservationKeys = Reservation.query(Reservation.endDateTime > datetime.now()).fetch(keys_only=True)
		ndb.delete_multi(deleteReservationKeys)

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

	# def get(self):


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
			deleteReservationKeys = Reservation.query(ancestor = deleteResourceKey).fetch(keys_only=True)
			# ndb.delete_multi(deleteResourceKey)
			# ndb.put_multi()
			# list_of_keys = ndb.Key(deleteReservations)
			# list_of_entities = ndb.get_multi(deleteReservationKeys)
			ndb.delete_multi(deleteReservationKeys)
			deleteResourceKey.delete()

		# nowDateTime = ndb.DateTimeProperty(auto_now_add=True)
		# startDateTime = ndb.DateTimeProperty()
		# 	datetime.strptime(Resource.startDateTime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
		# ).order(-Resource.modDate)
		# seconds = (datetime.now() - art.created).seconds

		# resource_query = Resource.query(
		# 	Resource.startDateTime
		# 	>=
		# 	datetime.now()
		# ).order(-Resource.startDateTime).order(-Resource.modDate)

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
		tagList1 = self.request.get('tags').strip().split(',')
		for tag in tagList1:
			if (tag is not None) and (tag.strip() != ""):
				resource.tags.append(tag.strip())
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
		sleep(0.2)

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
		resource.put()
		sleep(0.2)

		reservation.author = users.get_current_user()
		reservation.name = self.request.get('name')
		startDateTimeStr = self.request.get('startDateTime')
		endDateTimeStr = self.request.get('endDateTime')
		reservation.startDateTime = datetime.strptime(startDateTimeStr, '%Y-%m-%d %H:%M:%S')
		reservation.endDateTime = datetime.strptime(endDateTimeStr, '%Y-%m-%d %H:%M:%S')
		reservation.duration = (reservation.endDateTime - reservation.startDateTime).seconds
		reservation.put()
		sleep(0.2)
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

		resourceID = self.request.get('resourceID')
		resource = Resource()
		resource.author = users.get_current_user()
		resource.name = self.request.get('name')
		tagList1 = self.request.get('tags').strip().split(',')
		for tag in tagList1:
			if (tag is not None) and (tag.strip() != ""):
				resource.tags.append(tag.strip())

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
		sleep(0.2)

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
			resource = deleteReservationKey.parent().get()
			resource.numReservations = resource.numReservations - thisReservation.numsOfAttendee
			# thisResource.numReservations = thisResource.numReservations - thisReservation.numsOfAttendee
			resource.numsAvailable = resource.maxReservations - resource.numReservations
			resource.put()

			deleteReservationKey.delete()
			sleep(0.2)
		else:
			# resourceID = self.request.get('resourceID')
			# resource = Resource.query(urlsafe=resourceID).get()
			resourceID = self.request.get('resourceID')
			resource = ndb.Key(urlsafe=resourceID).get()

		# reservations = Reservation.query(ancestor=resource.key).fetch()

		deleteReservationKeys = Reservation.query(Reservation.startDateTime > datetime.now()).fetch(keys_only=True)
		ndb.delete_multi(deleteReservationKeys)

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

