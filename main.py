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

#Route to index page and present user's reservation
class MainPage(webapp2.RequestHandler):
	def get(self):
		"""login"""
		user = users.get_current_user()							#1
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'								#4
			url_createResource = 'Create Resource'
		else:
			self.redirect(users.create_login_url(self.request.uri))
		
		#Present user's reservation
		resource_query = Resource.query().order(-Resource.date)
		resources = resource_query.fetch()                      #2
		reservation_query = Reservation.query()
		reservations = reservation_query.fetch()                #3
		
		
		menu_title = 'see_your'
		deleteReservationID = ''
		deleteReservationID1 = self.request.get('deleteReservation')
		if deleteReservationID1 != '':
			deleteReservationID = deleteReservationID1
			reservation_query_delete = Reservation.query(Reservation.uuid == deleteReservationID)
			reservation_delete_key = reservation_query_delete.fetch()
			resource_query = Resource.query(Resource.uuid == reservation_delete_key[0].resourceUUID)
			resource = resource_query.fetch()
			resource[0].numReservations = resource[0].numReservations - 1
			reservation_delete_key[0].key.delete()
			query_params = {'menu_title': menu_title}
			self.redirect('/?' + urllib.urlencode(query_params))
		
		menu_title1 = self.request.get('menu_title')
		
		checkUserResources = 'false'
		checkUserResources1 = self.request.get('checkUserResources')
		if checkUserResources1 != '':
			checkUserResources = checkUserResources1
		
		getUser = ''							#7
		getUser1 = self.request.get('getUser')
		if getUser1 != '':
			checkUserResources = 'true'		#8
			getUser = getUser1
		
		if menu_title1 != '':
			menu_title = menu_title1
	########
		#Present index page
		context = {
			'user': user,          #1
			'url': url,
			'resources': resources,#2
			'reservations': reservations,#3
			'url_linktext': url_linktext,#4
			'url_createResource': url_createResource,#5
			'menu_title': urllib.quote_plus(menu_title),#6
			'getUser': getUser,#7
			'checkUserResources': checkUserResources,#8
		}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(context))
		
##########################################
class AddCreatedResource(webapp2.RequestHandler):
	@ndb.transactional(xg=True)
	def post(self):
		old_resource_uuid = self.request.get('resource_uuid');
		resource_name = self.request.get('resource_name')
		user = users.get_current_user().user_id()
		reservationbook_name = resource_name + user
		currDay = datetime.now().day
		currMonth = datetime.now().month
		currYear = datetime.now().year
		
		getDay = self.request.get('Day')
		getMonth = self.request.get('Month')
		getYear = self.request.get('Year')
		
		getDate = getMonth + '/' + getDay + '/' + getYear
		
		getStartHours = self.request.get('startHours')
		getStartMins = self.request.get('startMins')
		getStartMeridian = self.request.get('startMeridian')
		getStartTime = getStartHours + ':' + getStartMins + ' ' + getStartMeridian
		getStartDateTime = getDate + ' ' + getStartTime
		startDateTime = datetime.strptime(getStartDateTime, '%m/%d/%Y %I:%M %p')
		
		getEndHours = self.request.get('endHours')
		getEndMins = self.request.get('endMins')
		getEndMeridian = self.request.get('endMeridian')
		getEndTime = getEndHours + ':' + getEndMins + ' ' + getEndMeridian
		getEndDateTime = getDate + ' ' + getEndTime
		endDateTime = datetime.strptime(getEndDateTime, '%m/%d/%Y %I:%M %p')
		
		getTags = self.request.get('resource_Tag')
		getTagsList = getTags.split(';')
		
		if old_resource_uuid != "":
			resource_query = Resource.query(Resource.uuid == old_resource_uuid)
			resource_temp_key = resource_query.fetch()
			resource_temp_key[0].resourceName = resource_name
			resource_temp_key[0].startTime = startDateTime
			resource_temp_key[0].endTime = endDateTime
			resource_temp_key[0].tags = getTagsList
			resource_temp_key[0].put()
		
		else:
			addResource = Resource()
			addResource.resourceName = resource_name
			addResource.startTime = startDateTime
			addResource.endTime = endDateTime
			addResource.tags = getTagsList
			if users.get_current_user():
				addResource.user = User(
					identity=users.get_current_user().user_id(),
					email=users.get_current_user().email())
			
			addResource.uuid = str(uuid.uuid4())
			addResource.numReservations = 0
			addResource.put()
		
		menu_title = 'see_all'
		
		##
		
		query_params = {'menu_title': menu_title}
		self.redirect('/?' + urllib.urlencode(query_params))


class ReserveResource(webapp2.RequestHandler):
	@ndb.transactional(xg=True)
	def get(self):
		menu_title = 'show_reservations'
		menu_title1 = self.request.get('menu_title')
		flag = self.request.get('flag')
		
		if menu_title1 != '':
			menu_title = menu_title1
		resource_uuid = self.request.get('resource_uuid')
		
		resource_query = Resource.query(Resource.uuid == resource_uuid)
		resource = resource_query.fetch()
		resource_date = datetime.strftime(resource[0].startTime, '%m/%d/%Y')
		
		reservation_query = Reservation.query(Reservation.resourceUUID == resource_uuid)
		reservations = reservation_query.fetch()
		
		user = users.get_current_user()
		currDateTime = datetime
		
		if user:
			if user:
				url = users.create_logout_url(self.request.uri)
				url_linktext = 'Logout'
			
			context = {
				'user': user,
				'resource': resource[0],
				'url': url,
				'url_linktext': url_linktext,
				'menu_title': menu_title,
				'resource_date': resource_date,
				'reservations': reservations,
				'flag': flag,
				'currDateTime': 'currDateTime',
			}
			template = JINJA_ENVIRONMENT.get_template('reserveResource.html')
			self.response.write(template.render(context))
		else:
			self.redirect(users.create_login_url(self.request.uri))


class AddReservation(webapp2.RequestHandler):
	@ndb.transactional(xg=True)
	def post(self):
		
		menu_title = 'see_your'
		
		resource_name = self.request.get('resource_name')
		resource_uuid = self.request.get('resource_uuid')
		resource_startDate = self.request.get('resource_startDate')
		
		user = users.get_current_user()
		
		resource_query = Resource.query(Resource.uuid == resource_uuid)
		resource = resource_query.fetch()
		resource = resource[0]
		resource.date = datetime.now()
		resource.numReservations = resource.numReservations + 1
		
		resource.put()
		##
		
		reservation_query = Reservation.query(Reservation.resourceUUID == resource_uuid)
		reservations = reservation_query.fetch()
		
		getStartHours = self.request.get('startHours')
		getStartMins = self.request.get('startMins')
		getStartMeridian = self.request.get('startMeridian')
		getStartTime = getStartHours + ':' + getStartMins + ' ' + getStartMeridian
		getStartDateTime = resource_startDate + ' ' + getStartTime
		startDateTime = datetime.strptime(getStartDateTime, '%m/%d/%Y %I:%M %p')
		
		getEndHours = self.request.get('endHours')
		getEndMins = self.request.get('endMins')
		getEndTime = getEndHours + ':' + getEndMins
		endTime = datetime.strptime(getEndTime, '%H:%M')
		delta = timedelta(hours=endTime.hour, minutes=endTime.minute)
		endDateTime = startDateTime + delta
		flag = 'true'
		currentDate = datetime.now()
		
		if resource.startTime <= startDateTime:
			if resource.endTime >= endDateTime:
				for reservation in reservations:
					if reservation.startTime > startDateTime and reservation.startTime >= endDateTime:
						flag = 'true'
					else:
						if startDateTime >= reservation.endTime and endDateTime > reservation.endTime:
							flag = 'true'
						else:
							flag = 'false'
			else:
				flag = 'false'
		else:
			flag = 'false'
		
		if flag == 'true':
			addReservation = Reservation()
			addReservation.resourceName = resource_name
			addReservation.resourceUUID = resource_uuid
			addReservation.startTime = startDateTime
			addReservation.endTime = endDateTime
			addReservation.duration = getEndTime
			
			if users.get_current_user():
				addReservation.user = User(
					identity=users.get_current_user().user_id(),
					email=users.get_current_user().email())
			
			addReservation.uuid = str(uuid.uuid4())
			
			addReservation.put()
			##
			query_params = {'menu_title': menu_title}
			self.redirect('/?' + urllib.urlencode(query_params))
		else:
			menu_title = 'add_new_reservation'
			query_params = {'menu_title': menu_title, 'flag': flag, 'resource_uuid': resource_uuid}
			self.redirect('/reserveResource?' + urllib.urlencode(query_params))



class SearchResource(webapp2.RequestHandler):
	def get(self):
		resource_name = self.request.get('searchResource')
		resource_query = Resource.query(Resource.resourceName == resource_name)
		resources = resource_query.fetch()
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			
			context = {
				'user': user,
				'resources': resources,
				'url': url,
				'url_linktext': url_linktext
			}
			template = JINJA_ENVIRONMENT.get_template('searchResource.html')
			self.response.write(template.render(context))
		else:
			self.redirect(users.create_login_url(self.request.uri))


class ListTagResources(webapp2.RequestHandler):
	def get(self):
		get_Tag = self.request.get('get_Tag')
		resource_query = Resource.query(Resource.tags == get_Tag)
		resources = resource_query.fetch()
		user = users.get_current_user()
		
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			
			context = {
				'resources': resources,
				'user': user,
				'url': url,
				'url_linktext': url_linktext,
			}
			template = JINJA_ENVIRONMENT.get_template('seeTaggedResource.html')
			self.response.write(template.render(context))
		else:
			self.redirect(users.create_login_url(self.request.uri))

##########################################

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', AddCreatedResource),
	('/reserveResource', ReserveResource),
	('/addReservation', AddReservation),
	('/listTagResources', ListTagResources),
	('/searchResource', SearchResource),

], debug=True)

