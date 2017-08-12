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

from models import User
from models import Resource
from models import Reservation



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
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': 'Logout',
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

	# [END main_page]
		

##########################################




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


		#resource_name = self.request.get('resource_name', DEFAULT_RESOURCE_NAME)
		#resource_query = Resource.query(ancestor=)

		resource_query = Resource.query().order(-Resource.pubDate)
		resources = resource_query.fetch()



		# resources = Resource.query(ancestor=resource.key).order(-Resource.pubDate).fetch()

		template_values = {
			'resources': resources,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
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

		resource_query = Resource.query().order(-Resource.pubDate)
		resources = resource_query.fetch()

		template_values = {
			'resources': resources,
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}
		template = JINJA_ENVIRONMENT.get_template('myResource.html')
		self.response.write(template.render(template_values))

##################################################################


class CreateResource(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			self.redirect(users.create_login_url(self.request.uri))

		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
		}

		template = JINJA_ENVIRONMENT.get_template('createResource.html')
		self.response.write(template.render(template_values))


	def post(self):

		resource = Resource()
		# now = datetime.datetime.now()
		# print now.strftime("%Y/%m/%d")
		resource.pubDate = date.today().strftime("%Y/%m/%d")

		# >>> now.strftime("%B %d, %Y")
		# 'July 23, 2010'  '2014/12/25'

		resource.author = users.get_current_user()
		resource.resourceName = self.request.get('name')
		resource.tags = self.request.get('tags').strip().split(',')

		# resource.city = self.request.get('City')
		# resource.maxReservations = self.request.get('MaxAttendees')
		# resource.description = self.request.get('Description')
		resource.date = self.request.get('date')
		resource.startTime = self.request.get('startTime')
		resource.endTime = self.request.get('endTime')
		# resource.pubDate =

		resource.put()

		# url = '/AllResources?resourceID=%s' % resource.key.urlsafe()
		self.redirect('/CreateResource')

##################################################################


#
# class AddReservation(webapp2.RequestHandler):
# 	def get(self):
# 		user = users.get_current_user()
# 		if user:
# 			url = users.create_logout_url(self.request.uri)
# 			url_linktext = 'Logout'
# 		else:
# 			url = users.create_login_url(self.request.uri)
# 			url_linktext = 'Login'
#
# 		# guestbook_name = self.request.get('guestbook_name',
# 		# 								  DEFAULT_GUESTBOOK_NAME)
#
#
#
# 		template_values = {
# 			'user': user,
#
#
# 			'url': url,
# 			'url_linktext': url_linktext,
# 		}
#
# 		template = JINJA_ENVIRONMENT.get_template('createResource.html')
# 		self.response.write(template.render(template_values))
#
#
#
# 	def post(self):
#
# 		resourceID = self.request.get('resourceID')
# 		resource = ndb.Key(urlsafe=resourceID).get()
#
# 		if self.request.get('reservationID'):
# 			reservationID = self.request.get('reservationID')
# 			reservation = ndb.Key(urlsafe=reservationID).get()
# 		else:
# 			reservation = Reservation(parent=resource.key)
#
# 		resource.author = users.get_current_user()
# 		# answer.name = self.request.get('name')
# 		# answer.content = self.request.get('content')
# 		# answer.ups = 0
# 		# answer.downs = 0
# 		# answer.net = 0
#         #
#         #
# 		# answer.put()
# 		# url = '/ViewQuestion?questionID=%s' % question.key.urlsafe()
# 		# self.redirect(url)
#
#
# 		resource_Name = self.request.get('Name')
# 		resource_City = self.request.get('City', '')
# 		resource_Topics = self.request.get('Topics', '')
# 		resource_MaxAttendees = self.request.get('MaxAttendees', '')
# 		resource_Description = self.request.get('Description', '')
# 		resource_date = self.request.get('date', '')
# 		resource_startTime = self.request.get('startTime', '')
# 		resource_Description = self.request.get('endTime', '')
#
# 		qid = self.request.get('questionID')
# 		user = users.get_current_user()
# 		if user:
# 			url = users.create_logout_url(self.request.uri)
# 			url_linktext = 'Logout'
# 		else:
# 			url = users.create_login_url(self.request.uri)
# 			url_linktext = 'Login'
#
# 		# resource_query = Resource.query(Resource.uuid == old_resource_uuid)
#
#
# 		template_values = {
# 			'resource_Name': resource_Name,
#
# 			'resource_City': resource_City,
#
# 			'resource_Topics': resource_Topics,
#
# 			'resource_MaxAttendees': resource_MaxAttendees,
#
# 			'resource_Description': resource_Description,
#
# 			'resource_date': resource_date,
#
# 			'startTime': resource_startTime,
#
# 			'endTime': resource_startTime
# 		}
#
# 		template = JINJA_ENVIRONMENT.get_template('createResource.html')
# 		self.response.write(template.render(template_values))
##################################################################

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/CreateResource', CreateResource),
	('/AllResources', AllResources),
	('/MyResource', MyResource)

], debug=True)

