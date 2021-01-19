import webapp2
from google.appengine.ext import ndb
from google.appengine.api import images
import mimetypes
import logging

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    user_info= ndb.StringProperty()
    user_DOB=ndb.StringProperty()
    location=ndb.StringProperty()
    user_followers=ndb.StringProperty(repeated=True)
    user_following=ndb.StringProperty(repeated=True)
    file_name = ndb.StringProperty()
    cover_photo=ndb.StringProperty()
    blob = ndb.BlobProperty()
