import os
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles.finders import BaseFinder
from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

searched_locations = []


class IncludeFileFinder(BaseFinder):
    """
    A static files finder that uses the ``STATICFILES`` setting
    to locate files.
    """
    def __init__(self, app_names=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = OrderedDict()
        if not isinstance(settings.STATICFILES, (list, tuple)):
            raise ImproperlyConfigured("Your STATICFILES setting is not a tuple or list; ")
        for root in settings.STATICFILES:
            if isinstance(root, (list, tuple)):
                prefix, root = root
            else:
                prefix = ''
            if (prefix, root) not in self.locations:
                self.locations.append((prefix, root))
        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=os.path.dirname(root))
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage
        super(IncludeFileFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the extra locations
        as defined in ``STATICFILES``.
        """
        matches = []
        for prefix, root in self.locations:
            if root not in searched_locations:
                searched_locations.append(root)
            matched_path = self.find_location(os.path.dirname(root), path, prefix)
            if matched_path:
                if not all:
                    return matched_path
                if matched_path not in matches:
                    matches.append(matched_path)
        return matches

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
        path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            if os.path.exists(root):
                yield os.path.basename(root), storage
            else:
                print 'Warning File - %s - specified but not found on location %s' % (os.path.basename(root), root)
