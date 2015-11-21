import webapp2
import jinja2
import os
import logging

J_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

PROJECT_NAME = 'eatJapanBoston'

class BaseHandler(webapp2.RequestHandler):
    def handle_exception(self, exception, debug):
        # Log the error.
        logging.exception(exception)

        # Set a custom message.
        self.response.write('An error occurred.')

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)

class MainPage(BaseHandler):
    def get(self):
    	template = J_ENV.get_template('index.html')
    	template_values = {
    		'project_name':PROJECT_NAME,
    		'title':PROJECT_NAME,
    		'places':['a','b','c']
    		}
    	self.response.headers['Content-Type'] = 'text/html'
    	self.response.write(template.render(template_values))

class AboutPage(BaseHandler):
	def get(self):
		template = J_ENV.get_template('about.html')
		template_values = {
			'project_name':PROJECT_NAME,
			'title':'About',
			'places':['a','b','c']
			}
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

class PlacesPage(BaseHandler):
	def get(self):
		template = J_ENV.get_template('places.html')
		template_values = {
			'project_name':PROJECT_NAME,
			'title':'Places',
			'places':['a','b','c']
			}
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))
 
app = webapp2.WSGIApplication([
	(r'/about', AboutPage),
	webapp2.Route(r'/', handler=MainPage, name='home'),
	(r'/places', PlacesPage),
	],
	debug=True)


