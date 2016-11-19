from flask import jsonify, make_response, session, request
from flask_restful import Resource
from flask_session import Session
import json

class Mentions(Resource):
  # curl -i -H "Content-Type: application/json" -X GET -k cookie-jar  http://localhost:20500/Users
  def get(self):
    
    for piece in session:
      print piece
    if 'username' in session:
      response = {'endpoint': '/Users', 'verb':'get', 'status':'success'}
      responseCode = 200
    else:
      response = {'endpoint': '/Users', 'verb':'get', 'status':'failure'}
      responseCode = 401
    return make_response(jsonify(response), responseCode)
