from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
import json

class Speakzs(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k http://localhost:20500/Users/tom/Speakz
  def get(self, username):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}/Speakz'.format(username)), 'verb':'get', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Users/{0}/Speakz'.format(username)), 'verb':'get', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)
