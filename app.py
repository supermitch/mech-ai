import json
import os
import webapp2
from webapp2_extras import jinja2

from google.appengine.ext import ndb

class User(ndb.Model):
    """ Models a user of the system. Usernames are our only identifiers. """
    username = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

  def render_template(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))

class IndexHandler(BaseHandler):
  def get(self):
    self.render_template('index.html', name=self.request.get('name'))


class RegistrationHandler(webapp2.RequestHandler):
    def post(self):
        """ Generates and returns an access token for a POSTed username. """
        json_object = json.loads(self.request.body)
        if not 'username' in json_object:
            webapp2.abort(422, detail='Field "username" is required')

        username = json_object['username']
        exists = User.query(User.username==username).get()
        if not exists:
            print('USER NOT FOUND: {}'.format(username))
            user = User(username=username, access_token='434cat879')
            user.put()

        if exists:
            print('EXISTS: {}'.format(exists))
            content = {
                    'username': username,
                    'message': 'Failed: Username already exists',
            }
        else:
            content = {
                'username': username,
                'message': 'Success',
                'token': '435hfvbns93',
                'email': json_object.get('email', None)
            }
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(content))


class GamesHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write('Game Received')

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=IndexHandler, name='home', methods=['GET']),
    webapp2.Route('/register', handler=RegistrationHandler, name='registration', methods=['POST']),
    webapp2.Route('/games', handler=GamesHandler, name='games', methods=['POST']),
], debug=True)
