from google.appengine.ext import db

class SearchTerm(db.Model):
	"""Models a search term and its associated URLs."""
	term = db.StringProperty()
	urls = db.StringListProperty()
	
class Page(db.Model):
	"""Models a Page and its Daverank from the index."""
	text = db.TextProperty()
	url = db.StringProperty()
	url_rank = db.FloatProperty()
