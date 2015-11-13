import json
import os
import webapp2
from webapp2_extras import jinja2


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
        json_object = json.loads(self.request.body)
        self.response.write('Registration Received {}'.format(json_object))

class GamesHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write('Game Received')

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=IndexHandler, name='home', methods=['GET']),
    webapp2.Route('/register', handler=RegistrationHandler, name='registration', methods=['POST']),
    webapp2.Route('/games', handler=GamesHandler, name='games', methods=['POST']),
], debug=True)
