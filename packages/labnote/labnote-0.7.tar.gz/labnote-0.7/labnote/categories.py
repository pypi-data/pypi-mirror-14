"""
CategoryManager class definition
"""
import fnmatch
from collections import OrderedDict
from operator import attrgetter,itemgetter

class CategoryManager(OrderedDict):
    def __init__(self, categories):
        # Extend category metadata with defaults

        for k,v in categories.items():
            # Call _get_defaults() for each iteration to avoid need to do
            # a deep copy of the dict
            category = self._get_defaults()

            # Dict of category metadata
            if isinstance(v, dict):
                category.update(v)
            elif isinstance(v, list):
                # List of category patterns
                category['patterns'] = v

            categories[k] = category

        # Add blank "Other" category
        if 'Other' not in categories.keys():
            categories['Other'] = self._get_defaults()

        super().__init__(categories)

    def _get_category(self, entry, default='Other'):
        """Determines category for a given analysis"""
        for category,metadata in self.items():
            if any(fnmatch.fnmatch(entry.dir_name, ("*%s*" % p)) for p in
                    metadata['patterns']):
                return(category)
        return(default) 

    def add_entry(self, entry, category=None):
        """Adds a single entry to the CategoryManager"""
        if category is None:
            category = self._get_category(entry)
        self[category]['entries'].append(entry)

    def get_entries(self):
        """Returns a flattened list of all entries"""
        entries = []
        for category in self.values():
            entries = entries + category['entries']
        return(entries)

    def sort_entries(self):
        """Sorts entries within each category"""
        # Within each category, show most recently modified entries first
        for category in self:
            self[category]['entries'] = sorted(self[category]['entries'],
                                               key=attrgetter('date'),
                                               reverse=True)    

    def _get_defaults(self):
        """Gets default category metadata"""
        return {
           'entries': [], 
            'patterns': [],
            'description': "",
            'image': ""
        }
