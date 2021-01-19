from google.appengine.ext import ndb


class MyTwitter(ndb.Model):
    username = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now=True)
    user_tweets= ndb.StringProperty(repeated=True)
