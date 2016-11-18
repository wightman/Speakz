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

app = Flask(__name__)
# Set Server-side session config: Save sessions in the local app directory.
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'redis' # not tested!
app.config['SESSION_COOKIE_NAME'] = 'speakz.ca'
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

####################################################################################
#
# Routing: GET and POST using Flask-Session
#
# Demonstration only!
#
class Login(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "crap"}'
	#  	-c cookie-jar -k https://info3103.cs.unb.ca:61340/signin
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
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://info3103.cs.unb.ca:61340/signin
	def get(self):
		success = False
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://info3103.cs.unb.ca:61340/signin

	#
	#	Here's your chance to shine!
	#
	def delete(self):
		session.clear()
		return make_response(jsonify({'status': 'success'}), 200)

from Users import Users
####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Login, '/Login')
api.add_resource(Users,'/Users')
#api.add_resource(User,'/Users/{username}')
#api.add_resource(Speakzs,'/Users/{username}/Speakz')
#api.add_resource(Speakz,'/Users/{username}/Speakz/{speakzid}')
#api.add_resource(Following,'/Users/{username}/Following')
#api.add_resource(Followers,'/Users/{username}/Followers')
#api.add_resource(Mentions,'/Users/{username}/Mentions')
#api.add_resource(UserPreferences,'/Users/{username}/Preferences')
#api.add_resource(Hastags,'/Hashtag/{hashtag}')


#############################################################################
if __name__ == "__main__":
	#
	# Apache is minding the ssl
	#context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	#app.run(host=settings.APP_HOST, port=settings.APP_PORT, ssl_context=context, debug=settings.APP_DEBUG)
   	app.run(host=settings.APP_HOST, debug=settings.APP_DEBUG) # not tested
