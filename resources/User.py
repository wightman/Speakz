from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
import json

class User(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k http://localhost:20500/Users/tom
  def get(self, username):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'verb':'get', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'verb':'get', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)


  # curl -i -H "Content-Type: application/json" -X POST -d '{"post": "this website is awesome"}' -b cookie-jar -k http://localhost:20500/Users/tom
  def post(self, username):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'post':('{0}'.format(request.json['post'])), 'verb':'post', 'status':'success'}
      responseCode = 201
    else:
      response = {'endpoint': ('/Users/{0}'.format(username)), 'post':('{0}'.format(request.json['post'])), 'verb':'post', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)