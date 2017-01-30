from google.appengine.ext import db
from google.appengine.tools import bulkloader
import sys
sys.path.append('C:\Users\sameer\Documents\engine-repo')
from models import SearchTerm

class SearchTermLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'SearchTerm',
            [('term', str),
            ])
loaders = [SearchTermLoader]