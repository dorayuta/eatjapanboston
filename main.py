import webapp2
import jinja2
import os

J_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

PROJECT_NAME = 'eatJapanBoston'

class MainPage(webapp2.RequestHandler):
    def get(self):
    	template = J_ENV.get_template('index.html')
    	template_values = {'project_name':PROJECT_NAME}
    	self.response.headers['Content-Type'] = 'text/html'
    	self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
	('/', MainPage),
	],
	debug=True)


