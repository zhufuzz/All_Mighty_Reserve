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
from datetime import datetime, time, timedelta
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

DEFAULT_GUESTBOOK_NAME = "default_guest_book"

#Route to index page and present user's reservation
class MainPage(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name',
										  DEFAULT_GUESTBOOK_NAME)


		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': user,

			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

	# [END main_page]
		

##########################################



class AllResources(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name',
										  DEFAULT_GUESTBOOK_NAME)

		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': user,

			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))


class MyResource(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name',
										  DEFAULT_GUESTBOOK_NAME)

		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': user,

			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

##################################################################


class CreateResource(webapp2.RequestHandler):

	def get(self):
		guestbook_name = self.request.get('guestbook_name',
										  DEFAULT_GUESTBOOK_NAME)

		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': user,

			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}
		template = JINJA_ENVIRONMENT.get_template('createResource.html')
		self.response.write(template.render(template_values))

##################################################################

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/CreateResource', CreateResource)
	# ('/AllResources', AllResources)
	# ('/MyResource', MyResource)

], debug=True)

