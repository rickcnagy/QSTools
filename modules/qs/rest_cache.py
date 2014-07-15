#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Custom cache for the QS package, centered around caching REST responses."""


import qs


class RestCache(object):
    """Class for caching REST API responses."""

    def __init__(self):
        pass

    def get(self, key):
        """Access a key in the cache."""
        pass

    def set(self, key):
        """Set a key in the cache."""
        pass

    def invalidate(self, key=None):
        """Invalidate the cache.
        If key is supplied, only that key will be invalidated.
        """
        if key:
            _invalidate_key(key)
        else:
            _invalidate_cache()

    def _invalidate_key(self, key):
        """Invalidate a specific key."""
        pass

    def _invalidate_cache(self):
        """Invalidate the entire cache."""
        pass
