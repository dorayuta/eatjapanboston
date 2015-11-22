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
DEFAULT_GUIDE_NAME = 'default_guide_name'
_populated = False

template_values = {
	'project_name':PROJECT_NAME,
	}

# We set a parent key on the 'Guide' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.
def guide_key(guide_name=DEFAULT_GUIDE_NAME):
    # Constructs a Datastore key for a Gueide entity.
    # We use guide_name as the key.
    return ndb.Key('Guide', guide_name)

class Restaurant(ndb.Model):
    """A main model for representing an individual Guide entry."""
    name = ndb.StringProperty(indexed=False)
    # use yelp style ID for restaurant.
    ID = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

# manually populate restaurants
def populate():
	restaurant = Restaurant(parent=guide_key())
	restaurant.name = 'Pho Lovers'
	restaurant.ID = 'pho-lovers-sunnyvale'
	restaurant.content = 'Nice place for pho.'
	restaurant.put()
	getFavorites()

def clear():
	favorites_query = Restaurant.query(ancestor=guide_key())
	for fav in favorites_query:
		fav.key.delete()

def getFavorites():
	favorites_query = Restaurant.query(ancestor=guide_key())
	favorites = favorites_query.fetch(10)
	global template_values
	template_values['favorites'] = favorites

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
    	global _populated
    	# initialize restaurants?
    	if not _populated:
    		# need hosting script or something.
			clear()
			populate()
			_populated = True
			logging.info('Populating datastore.')

    	global template_values
    	template = J_ENV.get_template('templates/index.html')
    	template_values['title'] = PROJECT_NAME
    	self.response.headers['Content-Type'] = 'text/html'
    	self.response.write(template.render(template_values))

class AboutPage(BaseHandler):
	def get(self):
		global template_values
		logging.info(template_values)
		template = J_ENV.get_template('templates/about.html')
		template_values['title'] = 'About'
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

class FavoritesPage(BaseHandler):
	def get(self):
		with open('restaurants.json') as restaurants_file:
			restaurants = json.load(restaurants_file)
			logging.info(restaurants)
		global template_values
		template = J_ENV.get_template('templates/favorites.html')
		template_values['title'] = 'Favorites'
		template_values['restaurants'] = restaurants
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

class RestaurantPage(BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('<h1> Hellow </h1>')

app = webapp2.WSGIApplication([
	(r'/about', AboutPage),
	webapp2.Route(r'/', handler=MainPage, name='home'),
	(r'/favorites', FavoritesPage),
	(r'/favorites/.*', RestaurantPage)
	],
	debug=True)


