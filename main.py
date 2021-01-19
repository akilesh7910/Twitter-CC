import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from userPage import userPage
from uploadPic import uploadPic
from MyTwitter import MyTwitter
import datetime
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        if user == None:
            template_values = {
                'login' : users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('guest.html')
            self.respone.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser_temp = myuser_key.get()

        query = MyTwitter.query().fetch()

        if myuser_temp == None:

            template_values = {
                'logout' : users.create_logout_url(self.request.uri),
                'user' : myuser_temp,
                'header' : myuser_temp,
                'query' : query,
                'image' : myuser_temp.file_name
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

    def post(self):
        status='follow'
        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()

        if action == 'Submit':
            username = self.request.get('username')
            location = self.request.get('location')
            DOB = self.request.get('DOB')
            info = self.request.get('info')

            #self.response.write(myuser_temp)
            if username== '' or location== '' or DOB== '' :
                template_values = {
                    'error' : "Empty"
                }
                template = JINJA_ENVIRONMENT.get_template('login.html')
                self.response.write(template.render(template_values))

            elif username != '' or location != '' or DOB != '':

                query = MyUser.query(MyUser.username == username).fetch()

                if len(query)==0:

                     my_user = MyUser(id=user.user_id() , username=username.capitalize(), location=location.capitalize(),
                                          user_DOB=birthday, user_info = user_info.capitalize())
                     my_user.put()
                     template_values = {
                         'user': username,
                         'header': my_user,
                         'logout': users.create_logout_url(self.request.uri)
                     }
                     template = JINJA_ENVIRONMENT.get_template('main.html')
                     self.response.write(template.render(template_values))
                else:

                     template_values = {
                         'login': users.create_login_url(self.request.uri),
                         'error': "Username Already Exist."
                     }
                     template = JINJA_ENVIRONMENT.get_template('login.html')
                     self.response.write(template.render(template_values))

        if action == 'Tweet':

            user_tweet = self.request.get('tweet')
            if user_tweet == '':
               self.redirect('/')
            else:
                myuser_key = ndb.Key('MyTwitter',my_user.username )
                myuser = myuser_key.get()

                if myuser == None:
                    self.response.write('new ')
                    wordInfo = MyTwitter(id=my_user.username.capitalize(), username=my_user.username.capitalize(), timestamp=datetime.datetime.now())
                    wordInfo.user_tweets.append(user_tweet.lower())
                    wordInfo.put()
                    self.redirect('/')
                else:
                    myuser.user_tweets.append(user_tweet.lower())
                    myuser.put()
                    self.redirect('/')



        if action =='Search':
            list=[]
            response=[]
            search = self.request.get('search')

            if search == '':
                self.redirect('/')
            else:
                query_user = MyUser.query(MyUser.username == search.capitalize()).get()
                query_tweet = MyTwitter.query().fetch()
                if query_user is not None or len(query_tweet) > 0:


                    for i in query_tweet:
                        for k in i.user_tweets:
                            list.append(k)
                    for i in range(len(list)):
                        s1 = list[i].split(" ")
                        for x in s1:
                            if (x in search.lower()):
                                response.append(list[i])
                                break;


                    myuser_key = ndb.Key('MyUser', user.user_id())
                    myuser_following = myuser_key.get()

                    for i in myuser_following.user_following:

                        if i == query_user.username:
                            status = "Following"
                            break;

                    template_values = {
                        'user': my_user.username,
                        'header': my_user,
                        'logout': users.create_logout_url(self.request.uri),
                        'query_user': query_user,
                        'follow_status':status,
                        'query_tweet': response

                    }
                    template = JINJA_ENVIRONMENT.get_template('search.html')
                    self.response.write(template.render(template_values))

                elif len(query_user)== 0 :


                    template_values = {
                        'user': my_user.username,
                        'header': my_user,
                        'logout': users.create_logout_url(self.request.uri),
                        'query_error':'User Not Found'
                    }
                    template = JINJA_ENVIRONMENT.get_template('search.html')
                    self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
    ('/' , MainPage),('/userPage', userPage),('/uploadpic', uploadPic),
    ], debug=True)
