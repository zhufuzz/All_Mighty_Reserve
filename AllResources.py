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