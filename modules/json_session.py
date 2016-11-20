import json

class json_session():
  def get(self):
    json_session = {}
    with open('session.json') as data:
      json_session = json.load(data)
    return json_session