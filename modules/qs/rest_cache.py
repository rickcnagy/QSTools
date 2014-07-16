#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Custom caching for the QS package, centered around caching REST responses
in memory.
"""

import qs


class RestCache(object):
    """Interface for caching REST objects.

    Note that the objects returned are often the actual _data object, so
    generally the objects should be treated as read only to prevent corrupting
    the cache.
    """

    def __init__(self):
        self._data = self._default_data()

    def get(self):
        """Retrieve the entire cache."""
        return self._data

    def add(self, data):
        """Add data to the cache."""
        self._data = data

    def invalidate(self):
        """Invalidate the cache."""
        self._data = self._default_data()

    def _default_data(self):
        """The default value for _data after invalidation or __init__"""
        return None


class ListWithIDCache(RestCache):
    """A RestCache where self._data is a dict with the keys matching an id key
    in the contained dicts, but sends and receives data in flat lists.

    Args:
        id_key: The unique key that all entries in the dict will have - as in
            the id in 'list with id'.
        sort_key: An optional key to sort entries by when getting them.
    """

    def __init__(self, id_key='id', sort_key=None):
        super(ListWithIDCache, self).__init__()
        self._sort_key = sort_key
        self._id_key = id_key

    def get(self, identifier=None, by_id=False):
        """Return a flattened list of the data or a single entry by id if id is
        specified."""
        if not self._data: return self._data
        elif by_id: return self._data
        elif identifier: return self._data.get(qs.clean_id(identifier))
        else:
            return_data = [v for k, v in self._data.iteritems()]
            if self._sort_key:
                return sorted(return_data, key=lambda x: x[self._sort_key])
            return return_data

    def add(self, new_data):
        """Add to the cache with a list or single dict. Like list.append."""
        if type(new_data) not in [dict, list]:
            raise TypeError('new_data must be a dict or list, not {}'.format(
                type(new_data)))
        elif (type(new_data) is list
                and not all(type(i) is dict for i in new_data)):
            raise TypeError('new_data must contain only dicts')
        elif type(new_data) is dict:
            new_data = [new_data]

        self._data.update({qs.clean_id(i[self._id_key]): i for i in new_data})

    def _default_data(self):
        return {}
