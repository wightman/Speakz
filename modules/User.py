from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
from json_session import json_session
import json

class User(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -k cookie-jar  http://localhost:20500/Users/tom
  def get(self, username):
    #load json data from session
    session_data = json_session().get()

    if 'username' in session_data:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'verb':'get', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'verb':'get', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)


  # curl -i -H "Content-Type: application/json" -X POST -d '{"data": "this website is awesome"}' -k cookie-jar http://localhost:20500/Users/tom
  def post(self, username):
    #load json data from session
    session_data = json_session().get()

    if 'username' in session_data:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'data':('{0}'.format(request.json['data'])), 'verb':'post', 'status':'success'}
      responseCode = 201
    else:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'data':('{0}'.format(request.json['data'])), 'verb':'post', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)