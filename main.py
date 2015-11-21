import webapp2
import jinja2
import os
import logging

from google.appengine.ext import ndb

J_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

Logger = logging.getLogger('all')
Logger.debug('!!!!!!!!!!!!!!!!!!!!!!!!')
PROJECT_NAME = 'eatJapanBoston'
DEFAULT_GUIDE_NAME = 'default_guide_name'

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

def populate():
	restaurant = Restaurant(parent=guide_key())
	restaurant.name = 'Pho Lovers'
	restaurant.ID = 'pho-lovers-sunnyvale'
	restaurant.content = 'Nice place for pho.'
	restaurant.put()

def clear():
	favorites_query = Restaurant.query(ancestor=guide_key())
	for fav in favorites_query:
		fav.key.delete()

favorites_query = Restaurant.query(ancestor=guide_key())
favorites = favorites_query.fetch(10)

template_values = {
	'project_name':PROJECT_NAME,
	'favorites':favorites
	}

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
    	global template_values
    	template = J_ENV.get_template('index.html')
    	template_values['title'] = 'Home'
    	self.response.headers['Content-Type'] = 'text/html'
    	self.response.write(template.render(template_values))

class AboutPage(BaseHandler):
	def get(self):
		global template_values
		template = J_ENV.get_template('about.html')
		template_values['title'] = 'About'
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))

class FavoritesPage(BaseHandler):
	def get(self):
		global template_values
		template = J_ENV.get_template('favorites.html')
		template_values['title'] = 'Favorites'
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(template.render(template_values))
 
# populate()
clear()

app = webapp2.WSGIApplication([
	(r'/about', AboutPage),
	webapp2.Route(r'/', handler=MainPage, name='home'),
	(r'/favorites', FavoritesPage),
	],
	debug=True)


