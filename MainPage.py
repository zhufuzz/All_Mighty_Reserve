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
