
import webapp2
import jinja2
import mimetypes
import logging
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

from myuser import MyUser

from uploadPic import uploadPic
from MyTwitter import MyTwitter


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class userPage(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        user_nameLength = ""
        status=""

        userinfo=""
        response=False

        userKey=""
        followersresponse=False
        userQueryunfollow=''

        following=[]
        follower=[]

        status = "Follow"

        userUnFollow=[]
        user_followers=[]

        u=''
        val=0
        updateResponse=0



        if user == None:
            template_values = {
                'login': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()

        if my_user == None:
            template_values = {
                'login': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))

        else:
             username= self.request.get('username')
             user_following = self.request.get('user_following')
             user_unfollowing=self.request.get('unfollowing')
             delete_tweet=self.request.get('delete_tweet')
             query = MyUser.query(MyUser.username == my_user.username).get()

             if len(username) > 0:
                userQuery = MyUser.query(MyUser.username == username).fetch()
                user_nameLength = username
                for i in userQuery:
                    userinfo = i

             if len(user_following) > 0:
                userQueryfollow = MyUser.query(MyUser.username == user_following).fetch()
                user_nameLength = user_following
                for i in userQueryfollow:
                    userinfo = i

             if len(user_unfollowing) > 0:
                 userQueryunfollow = MyUser.query(MyUser.username == my_user.username).fetch()
                 user_nameLength =  userQueryunfollow

             if len(user_nameLength) == 0 or username == my_user.username:

                myuser_key = ndb.Key('tweets', my_user.username)
                userProfile = myuser_key.get()


                if userProfile is not None:

                     val=range(len(userProfile.user_tweets))

                elif userProfile is None:
                    val=0

                template_values = {
                    'logout': users.create_logout_url(self.request.uri),
                    'user': query,
                    'header': query,
                    'userTitle': query.username,  #
                    'test': 0,
                    'following': len(query.user_following),
                    'follower': len(query.user_followers),
                    'followStatus': 'Edit Profile',
                    'unfollowstatus': '',
                    'range': val,
                    'user_tweets': userProfile,
                    'option': 'block',
                    'upload_url': format(blobstore.create_upload_url('/uploadpic')),
                    'image': query.file_name,
                    'image_cover': query.cover_photo

                }
                template = JINJA_ENVIRONMENT.get_template('userPage.html')
                self.response.write(template.render(template_values))
             else:
                 if len(username) > 0:
                     for i in  query.user_followers:

                         if i == username:
                             status="Following"
                             break;
                     myuser_key = ndb.Key('MyTwitter', username)
                     userProfile = myuser_key.get()
                     template_values = {
                         'logout': users.create_logout_url(self.request.uri),
                         'user': userinfo,
                         'header': query,
                         'userTitle':username,
                         'test': len(username),
                         'following': len(query.user_following),
                         'follower': len(query.user_followers),
                         'followStatus':status,
                         'range': range(len(userProfile.user_tweets)),
                         'unfollowstatus':'Unfollow ',
                         'user_tweets': userProfile,
                         'option': 'none',
                         'image': query.file_name,
                         'image_cover': query.cover_photo

                     }
                     template = JINJA_ENVIRONMENT.get_template('userPage.html')
                     self.response.write(template.render(template_values))

                 if len(user_following) > 0:
                     if user_following:
                        query = MyUser.query(MyUser.username == my_user.username).get()
                        user_retrieve=MyUser.query(MyUser.username == user_following).fetch()
                        myuser_key = ndb.Key('MyTwitter', user_following)
                        userProfile = myuser_key.get()

                        if userProfile is not None:
                            updateResponse = range(len(userProfile.user_tweets))

                        for i in user_retrieve:
                            userKey=i

                        if len(query.user_following) == 0:

                            wordInfo = MyUser(id=user.user_id(), username=query.username, user_info=query.user_info,
                                              location=query.location, user_DOB=query.user_DOB, cover_photo=query.cover_photo, file_name=query.file_name)
                            wordInfo.user_following.append(user_following.capitalize())
                            wordInfo.put()

                            userKey.user_followers.append(query.username)
                            userKey.put()
                        else:
                            for i in query.user_following:
                                if i == user_following:
                                    response = True
                                    break
                            for j in userKey.user_followers:
                              if j == query.username:
                                 followersresponse=True
                                 break

                            if response == False:
                                query.user_following.append(user_following.capitalize())
                                query.put()

                            if followers_response == False:
                                userKey.user_followers.append(query.username)
                                userKey.put()


                        template_values = {
                            'logout': users.create_logout_url(self.request.uri),
                            'user': userinfo,
                            'header': query,
                            'userTitle': user_following,
                            'following': len(query.user_following),
                            'follower': len(query.user_followers),
                            'test': len(user_following),
                            'followstatus': 'Following',
                            'range': updateResponse,
                            'unfollowstatus': 'Unfollow ',
                            'user_tweets': userProfile,
                            'option': 'none',
                            'image': query.file_name,
                            'image_cover': query.cover_photo

                        }
                        template = JINJA_ENVIRONMENT.get_template('userPage.html')
                        self.response.write(template.render(template_values))

                 if len(user_unfollowing) > 0:
                     userUnfollowRetrieve = MyUser.query(MyUser.username == my_user.username).fetch()
                     retrieveUnfollowUserInfo = MyUser.query(MyUser.username == user_unfollowing).get()
                     myuser_key = ndb.Key('MyTwitter', userUnfollowing)
                     userProfile = myuser_key.get()

                     if userProfile is not None:
                         updateResponse = range(len(userProfile.user_tweets))

                     for i in userUnfollowRetrieve:
                         user_unFollow = i.user_unfollowing

                     user_followers=retrieveUnfollowUserInfo.user_followers
                     user_unFollow.remove(user_unfollowing)
                     user_followers.remove(my_user.username)
                     wordInfo = MyUser(id=user.user_id(), username=my_user.username, user_info=my_user.user_info,
                                       location=my_user.location, user_DOB=my_user.user_DOB, user_following=user_unFollow, user_followers=my_user.user_followers, cover_photo=my_user.cover_photo, file_name=my_user.file_name)
                     wordInfo.put()

                     friendInfo = MyUser(id=retrieveUnfollowUserInfo.key.id(), username=retrieveUnfollowUserInfo.username, user_info=retrieveUnfollowUserInfo.user_info,
                                         location=retrieveUnfollowUserInfo.location, user_DOB=retrieveUnfollowUserInfo.user_DOB,
                                         user_following=retrieveUnfollowUserInfo.user_following, user_followers=user_followers, cover_photo=retrieveUnfollowUserInfo.cover_photo, file_name=retrieveUnfollowUserInfo.file_name)
                     friendInfo.put()


                     query = MyUser.query(MyUser.username == user_unfollowing).fetch()
                     for i in query:
                         following = i.user_following
                         follower = i.user_followers
                         userinfo=i
                     template_values = {
                         'logout': users.create_logout_url(self.request.uri),
                         'user': userinfo,
                         'header': my_user,
                         'userTitle': userUnfollowing,
                         'following': len(following),
                         'follower': len(follower),
                         'test': len(user_unfollowing),
                         'followStatus': 'Follow',
                         'range': updateResponse,
                         'unfollowstatus':'',
                         'user_tweets': userProfile,
                         'option': 'none'

                     }
                     template = JINJA_ENVIRONMENT.get_template('userPage.html')
                     self.response.write(template.render(template_values))


    def post(self):

        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()
        updateResponse = 0

        query = MyUser.query(MyUser.username == my_user.username).get()
        if action == 'UPDATE':
            myuser_key = ndb.Key('MyTwitter', my_user.username)
            userProfile = myuser_key.get()

            if userProfile is not None:
                updateResponse=range(len(userProfile.user_tweets))
            userName = self.request.get('username')
            userLocation = self.request.get('location')
            user_birthday = self.request.get('DOB')
            userinfo = self.request.get('info')

            userInfo = MyUser(id=user.user_id(), username=userName.capitalize(), user_info=userinfo.capitalize(),
                              user_DOB=user_birthday, location=userLocation.capitalize(), cover_photo=query.cover_photo, file_name=query.file_name)
            userInfo.put()

            template_values = {
                'response': "Edit Successful",
                'logout': users.create_logout_url(self.request.uri),
                'header': query,
                'userTitle': userName,
                'user': query,
                'following': len(query.user_following),
                'follower': len(query.user_followers),
                'followStatus': 'Edit Profile',
                'range': updateResponse,
                'test': 0,
                'user_tweets': userProfile,
                'info': query.user_info,
                'image': query.file_name,
                'image_cover': query.cover_photo

            }
            template = JINJA_ENVIRONMENT.get_template('userPage.html')
            self.response.write(template.render(template_values))

        if action=='Edit':
            tweetNumber = self.request.get('hidden')
            val=int(tweetNumber)
            queryTweet = MyTwitter.query(MyTwitter.username == my_user.username).get()
            template_values = {
                'response': "Edit Successful",
                'logout_url': users.create_logout_url(self.request.uri),
                'header': query,
                'userTitle': query.username,
                'user': query,
                'following': len(query.user_following),
                'follower': len(query.user_followers),
                'followStatus': 'Edit Profile',
                'range': range(len(queryTweet.user_tweets)),
                'test': 0,
                'user_tweets': queryTweet,
                'tweetEdit':queryTweet.user_tweets[val],
                'info': query.user_info,
                'showEditTweet':'block',
                'tweetnumber':tweetNumber,
                'image': query.file_name,
                'image_cover': query.cover_photo
            }
            template = JINJA_ENVIRONMENT.get_template('userPage.html')
            self.response.write(template.render(template_values))
        if action =='Update Tweet':
            temp = []
            tweetNumber = self.request.get('tweetnumber')
            val=int(tweetNumber)
            editedTweet=self.request.get('tweetEdit')

            queryTweet = MyTwitter.query(MyTwitter.username == my_user.username).get()
            temp=queryTweet.user_tweets
            temp[val]=editedTweet
            usertweet = MyTwitter(id=my_user.username, user_tweets=temp, username=my_user.username)
            usertweet.put()
            template_values = {
                'response': "Edit Successful",
                'logout': users.create_logout_url(self.request.uri),
                'header': query,
                'userTitle':query.username ,
                'user': query,
                'following': len(query.user_following),
                'follower': len(query.user_followers),
                'followStatus': 'Edit Profile',
                'range': range(len(queryTweet.user_tweets)),
                'test': 0,
                'user_tweets': queryTweet,
                'tweetEdit': queryTweet.user_tweets[val],
                'info': query.user_info,
                'showEditTweet': 'none',
                'tweetnumber': tweetNumber,
                'image': query.file_name,
                'image_cover': query.cover_photo
            }
            template = JINJA_ENVIRONMENT.get_template('userPage.html')
            self.response.write(template.render(template_values))
        if action =='Delete':
            temp = []
            tweetNumber = self.request.get('deleteTweet')
            val = int(tweetNumber)
            queryTweet = MyTwitter.query(Twitter.username == my_user.username).get()
            temp = queryTweet.user_tweets
            temptweet = temp[val]

            temp.remove(temptweet)
            if not temp:
                self.redirect('/userPage')
            else:
                usertweet = MyTwitter(id=my_user.username, user_tweets=temp, username=my_user.username)
                usertweet.put()
                template_values = {
                    'response': "Edit Successful",
                    'logout': users.create_logout_url(self.request.uri),
                    'header': query,
                    'userTitle': query.username,
                    'user': query,
                    'following': len(query.user_following),
                    'follower': len(query.user_followers),
                    'followStatus': 'Edit Profile',
                    'range': range(len(queryTweet.user_tweets)),
                    'test': 0,
                    'user_tweets': queryTweet,
                    'tweetEdit': queryTweet.user_tweets[val],
                    'info': query.user_info,
                    'showEditTweet': 'none',
                    'tweetnumber': tweetNumber,
                    'image': query.file_name,
                    'image_cover': query.cover_photo
                }
                template = JINJA_ENVIRONMENT.get_template('userPage.html')
                self.response.write(template.render(template_values))
