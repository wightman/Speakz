from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
import json

class Speakz(Resource):
  # curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar -k http://localhost:20500/Users/tom/Speakz/1
  def delete(self, username, speakzid):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}/Speakz/{1}'.format(username, speakzid)), 'verb':'delete', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Users/{0}/Speakz/{1}'.format(username, speakzid)), 'verb':'delete', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)

  # curl -i -H "Content-Type: application/json" -X PUT -d '{"post": "edited post"}' -b cookie-jar -k http://localhost:20500/Users/tom/Speakz/1
  def put(self, username, speakzid):
    if 'username' in session:
      response = {'endpoint': ('/Users/{0}/Speakz/{1}'.format(username, speakzid)), 'post':('{0}'.format(request.json['post'])), 'verb':'put', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': ('/Users/{0}/Speakz/{1}'.format(username, speakzid)), 'post':('{0}'.format(request.json['post'])), 'verb':'put', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)
