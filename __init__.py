#!/usr/bin/env python
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
#import ldap

# Apache looks after ssl
#import ssl #include ssl libraries

import settings # Our server and db settings, stored in settings.py

# force std to use utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__, static_url_path="")
# Application's Secret key is set in /var/www/speakz/speakz.wsgi
#app.secret_key = settings.SECRET_KEY

#app.config['SESSION_TYPE'] = 'redis' # not tested!
app.config['SESSION_TYPE'] = 'filesystem' #
app.config['SESSION_COOKIE_NAME'] = settings.APP_HOST
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
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


#
#	Default hit returns the client application
#
@app.route('/')
def root():
	return app.send_static_file('index.html')

####################################################################################
#
# Routing: GET and POST using Flask-Session
#
#
class Login(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "crap"}' -c cookie-jar https://speakz.ca/signin
	#
	def post(self):

		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
 		try:
 			# Check for required attributes in json document, create a dictionary
	 		parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				l = ldap.open(settings.LDAP_HOST)
				l.start_tls_s()
				l.simple_bind_s("uid="+request_params['username']+
					", ou=People,ou=fcs,o=unb", request_params['password'])
				# At this point we have sucessfully authenticated.

				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201
			except ldap.LDAPError, error_message:
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				l.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar  https://speakz.ca/Login
	def get(self):
		success = False
		if 'username' in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 404

		return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar https://speakz.ca/signin

	def delete(self):
		if 'username' in session:
			session.clear()
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 404
		return make_response(jsonify(response), responseCode)


from modules.Users import Users
from modules.User import User
from modules.Speakzs import Speakzs
from modules.Speakz import Speakz
from modules.Following import Following
from modules.Followers import Followers
from modules.Mentions import Mentions
from modules.UserPreference import UserPreference
from modules.Hashtags import Hashtags
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
	#
	# Apache is minding the ssl
   	app.run()
