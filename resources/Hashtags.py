from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
import json

class Hashtags(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -b cookie-jar -k http://localhost:20500/Hashtag/unb
  def get(self, hashtag):
    if 'username' in session:
      response = {'endpoint': ('/Hashtag/{0}'.format(hashtag)), 'verb':'get', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Hashtag/{0}'.format(hashtag)), 'verb':'get', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)
