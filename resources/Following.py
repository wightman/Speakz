from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
import json

class Following(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k http://localhost:20500/Users/tom/Following
  def get(self, username):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}/Following'.format(username)), 'verb':'get', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Users/{0}/Following'.format(username)), 'verb':'get', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)


  # follow a user
  # curl -i -H "Content-Type: application/json" -X POST -d '{"following": "jleemur"}' -b cookie-jar -k http://localhost:20500/Users/tom/Following
  def post(self, username):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}/Following'.format(username)), 'following':('{0}'.format(request.json['following'])), 'verb':'post', 'status':'success'}
      responseCode = 201
    else:
      response = {'endpoint': ('/Users/{0}/Following'.format(username)), 'following':('{0}'.format(request.json['following'])), 'verb':'post', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)
