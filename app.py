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
app.config['SESSION_COOKIE_NAME'] = 'speakz'
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
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Tom", "password": "crapcrap"}' -c cookie-jar  http://localhost:20500/Login
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
			# Three dummy accounts for testing only.
			username = request_params['username']
			password = request_params['password']

			login = False
			if username == 'Tom' and password == 'crapcrap':
				login = True
			elif username == 'Dick' and password == 'crapcrap':
				login = True
			elif username == 'Mary' and password == 'crapcrap':
				login = True
			if(login):
				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201
			else:
				response = {'status': 'Access denied'}
				responseCode = 403
		for piece in session:
			print session
		return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE
	#  	-k cookie-jar  http://localhost:20500/Login
	def delete(self):
		session.clear()
		return make_response(jsonify({'status': 'success'}), 200)


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
	# Running in a local testing context - no ssl needed.
	#context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
   	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
