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


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!\nWelcome to Mech AI.')

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
], debug=True)
