from flask import jsonify, make_response, session
from flask_restful import Resource
from flask_session import Session
from json_session import json_session
import json

class Users(Resource):
	# curl -i -H "Content-Type: application/json" -X GET -c cookie-jar -k http://localhost:20500/Users
	def get(self):
    #load json data from session
		session_data = json_session().get()

		if 'username' in session_data:
			response = {'endpoint': '/Users', 'verb':'get', 'status':'success'}
			responseCode = 200
		else:
			response = {'endpoint': '/Users', 'verb':'get', 'status':'failure'}
			responseCode = 401
		return make_response(jsonify(response), responseCode)