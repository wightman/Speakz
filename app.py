#!/usr/bin/env python
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
import settings # Our server and db settings, stored in settings.py

# force std to use utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'speakz.ca'
Session(app)


####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)


from resources.Login import Login
from resources.Users import Users
from resources.User import User
from resources.Speakzs import Speakzs
from resources.Speakz import Speakz
from resources.Following import Following
from resources.Followers import Followers
from resources.Mentions import Mentions
from resources.UserPreference import UserPreference
from resources.Hashtags import Hashtags
####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Login, '/Login')
api.add_resource(Users,'/Users')
api.add_resource(User,'/Users/<string:username>')
api.add_resource(Speakzs,'/Users/<string:username>/Speakz')
api.add_resource(Speakz,'/Users/<string:username>/Speakz/<int:speakzid>')
api.add_resource(Following,'/Users/<string:username>/Following')
api.add_resource(Followers,'/Users/<string:username>/Followers')
api.add_resource(Mentions,'/Users/<string:username>/Mentions')
api.add_resource(UserPreference,'/Users/<string:username>/Preference')
api.add_resource(Hashtags,'/Hashtag/<string:hashtag>')


#############################################################################
if __name__ == "__main__":
	# Running in a local testing context - no ssl needed.
	#context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
   	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
