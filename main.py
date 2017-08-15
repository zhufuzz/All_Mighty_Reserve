"""
main.py

"""

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
		user = users.get_current_user()
		url, url_linktext = checkUser(user, self)

		# reservations = Reservation.query(user == Reservation.author).order(-Reservation.pubDate).fetch()


		# resource_query = Resource.query(Reservation.)
		# .filter(Reservation.endTime.date() >= date.today())


		template_values = {
			# 'reservations': reservations,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'today': date.today()
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

	# [END main_page]
		

##########################################




class AllResources(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		url, url_linktext = checkUser(user, self)

		resource_query = Resource.query().order(-Resource.modDate)
		resources = resource_query.fetch()

		template_values = {
			'resources': resources,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'today': date.today()

		}
		template = JINJA_ENVIRONMENT.get_template('allResources.html')
		self.response.write(template.render(template_values))


##########################################

#
# class MyResource(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		url, url_linktext = checkUser(user, self)
#
# 		resource_query = Resource.query().order(-Resource.modDate)
# 		resources = resource_query.fetch()
#
# 		template_values = {
# 			'resources': resources,
# 			'user': user,
# 			'url': url,
# 			'url_linktext': url_linktext,
# 			'today': date.today()
#
# 		}
# 		template = JINJA_ENVIRONMENT.get_template('myResource.html')
# 		self.response.write(template.render(template_values))


##################################################################

# @ndb.transactional
class CreateResource(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		url, url_linktext = checkUser(user, self)

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}

		# if self.request.get('resourceID'):
		# 	resourceID = self.request.get('resourceID')
		# 	resource = ndb.Key(urlsafe=resourceID).get()
		# 	template_values['resource'] = resource

		template = JINJA_ENVIRONMENT.get_template('createResource.html')
		self.response.write(template.render(template_values))


	def post(self):
		# if self.request.get('resourceID'):
		# 	resourceID = self.request.get('resourceID')
		# 	resource = ndb.Key(urlsafe=resourceID).get()
		# else:
		# 	resource = Resource()
		resource = Resource()
		resource.author = users.get_current_user()
		resource.name = self.request.get('name')
		resource.tags = self.request.get('tags').strip().split(',')
		resource.maxReservations = int(self.request.get('maxReservations'))
		resource.numsAvailable = int(self.request.get('maxReservations'))
		resource.numReservations = 0

		resource.description = self.request.get('description')

		# dateStr = self.request.get('date')
		startTimeStr = self.request.get('startTime')
		endTimeStr = self.request.get('endTime')

		# resource.date = datetime.strptime(dateStr, '%Y/%m/%d')
		# resource.startTime = datetime.strptime(dateStr + ' ' + startTimeStr, '%Y/%m/%d %H:%M')
		# resource.endTime = datetime.strptime(dateStr + ' ' + endTimeStr, '%Y/%m/%d %H:%M')

		resource.startTime = datetime.strptime(startTimeStr, "dd MM yyyy - HH:ii p")
		resource.endTime = datetime.strptime(endTimeStr, "dd MM yyyy - HH:ii p")

		# resource.city = self.request.get('City')
		# resource.maxReservations = self.request.get('MaxAttendees')
		# resource.description = self.request.get('Description')

		# resource.pubDate =

		resource.put()
		# query_params = {'': ''}

		# url = '/AllResources?resourceID=%s' % resource.key.urlsafe()
		# query_params = {'resourceID': resource.key.urlsafe()}
		# + urllib.urlencode(query_params)
		# url = '/'

		# self.redirect('/AllResources?'+urllib.urlencode(query_params))
		# self.redirect('/AllResources?'+urllib.urlencode(query_params))
		url = '/AllResources?resourceID=%s' % resource.key.urlsafe()
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
		user = users.get_current_user()
		url, url_linktext = checkUser(user, self)

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
			'today': date.today()
		}
		template = JINJA_ENVIRONMENT.get_template('reserve.html')
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
		# dateStr = self.request.get('date').strip()
		startTimeStr = self.request.get('startTime')
		endTimeStr = self.request.get('endTime')

		dateStr = resource.date.strftime('%Y/%m/%d')

		reservation.date = datetime.strptime(dateStr, '%Y/%m/%d')

		reservation.startTime = datetime.strptime(dateStr + ' ' + startTimeStr, '%Y/%m/%d %H:%M')
		reservation.endTime = datetime.strptime(dateStr + ' ' + endTimeStr, '%Y/%m/%d %H:%M')

		reservation.duration = (reservation.endTime - reservation.startTime).seconds
		reservation.put()


		url = '/A?resourceID=%s' % resource.key.urlsafe()
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


# class EditResource(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		url, url_linktext = checkUser(user, self)
#
# 		template_values = {
# 			'user': user,
# 			'url': url,
# 			'url_linktext': url_linktext,
# 		}
#
# 		if self.request.get('resourceID'):
# 			resourceID = self.request.get('resourceID')
# 			resource = ndb.Key(urlsafe=resourceID).get()
# 			template_values['resource'] = resource
#
# 		template = JINJA_ENVIRONMENT.get_template('createResource.html')
# 		self.response.write(template.render(template_values))
#
#
# 	def post(self):
# 		if self.request.get('resourceID'):
# 			resourceID = self.request.get('resourceID')
# 			resource = ndb.Key(urlsafe=resourceID).get()
# 		else:
# 			resource = Resource()
#
# 		resource.author = users.get_current_user()
# 		resource.name = self.request.get('name')
# 		resource.tags = self.request.get('tags').strip().split(',')
# 		resource.maxReservations = int(self.request.get('maxReservations'))
# 		resource.numsAvailable = int(self.request.get('maxReservations'))
# 		resource.numReservations = 0
#
# 		resource.description = self.request.get('description')
#
# 		dateStr = self.request.get('date')
# 		startTimeStr = self.request.get('startTime')
# 		endTimeStr = self.request.get('endTime')
#
# 		resource.date = datetime.strptime(dateStr, '%Y/%m/%d')
# 		resource.startTime = datetime.strptime(dateStr + ' ' + startTimeStr, '%Y/%m/%d %H:%M')
# 		resource.endTime = datetime.strptime(dateStr + ' ' + endTimeStr, '%Y/%m/%d %H:%M')
#
#
# 		# resource.city = self.request.get('City')
# 		# resource.maxReservations = self.request.get('MaxAttendees')
# 		# resource.description = self.request.get('Description')
#
# 		# resource.pubDate =
#
# 		resource.put()
# 		# query_params = {'': ''}
#
# 		# url = '/AllResources?resourceID=%s' % resource.key.urlsafe()
# 		query_params = {'resourceID': resource.key.urlsafe()}
# 		# + urllib.urlencode(query_params)
# 		# url = '/'
#
# 		# self.redirect('/AllResources?'+urllib.urlencode(query_params))
# 		self.redirect('/AllResources?'+urllib.urlencode(query_params))
#


##################################################################

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/CreateResource', CreateResource),
	('/AllResources', AllResources),
	# ('/DeleteResource', DeleteResource),
    #
	# ('/MyResource', MyResource),
	# ('/DeleteReservation', DeleteReservation),
	# ('/ReserveBase', ReserveBase),
    #
	# ('/Reservations', Reservations),
	# ('/Reserve', Reserve),
	# ('/EditResource', EditResource),

], debug=True)

