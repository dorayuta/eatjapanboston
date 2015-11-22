import jinja2
import json
import logging
from google.appengine.ext import ndb
import os
import webapp2

logging.basicConfig(format='%(asctime)s %(message)s', filename='main.log', level=logging.DEBUG)
logging.debug('This message should go to the log file.')
logging.info('Logging info.')
logging.warning('Logging warning.')

J_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

PROJECT_NAME = 'eatJapanBoston'

with open('restaurants.json') as restaurants_file:
	restaurants = json.load(restaurants_file)

template_values = {
	'project_name':PROJECT_NAME,
	# dictionaries of restaurants sorted by....
	'restaurants': sorted(restaurants.values())
	}

# helper to get restaurant info from ID
def restaurantFromID(ID):
	for restaurant in template_values['restaurants']:
		if restaurant['ID'] == ID:
			return restaurant
	raise KeyError("Restaurant ID {} is invalid.".format(ID))

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
    	logging.debug("what's going on?")
    	global template_values
    	logging.info(template_values)
    	template = J_ENV.get_template('templates/index.html')
    	template_values['title'] = PROJECT_NAME
    	self.response.headers['Content-Type'] = 'text/html'
    	self.response.write(template.render(template_values))

class AboutPage(BaseHandler):
	def get(self):
		global template_values
		template = J_ENV.get_template('templates/about.html')
		template_values['title'] = 'About'
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

class FavoritesPage(BaseHandler):
	def get(self):
		global template_values
		template = J_ENV.get_template('templates/favorites.html')
		template_values['title'] = 'Favorites'
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

class RestaurantPage(BaseHandler):
	def get(self, restaurant_id):
		global template_values
		template = J_ENV.get_template('templates/restaurant.html')
		logging.debug(restaurant_id)
		restaurant = restaurantFromID(restaurant_id)
		template_values['restaurant'] = restaurant
		template_values['title'] = restaurant['name']
		template_values['address'] = restaurant['address']
		template_values['root_path'] = '../{}'
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
	(r'/about', AboutPage),
	webapp2.Route(r'/', handler=MainPage, name='home'),
	(r'/favorites', FavoritesPage),
	(r'/favorites/(.*)', RestaurantPage)
	],
	debug=True)


