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
        self._data = None

    def get(self):
        """Retrieve the entire cache."""
        return self._data

    def add(self, data):
        """Add data to the cache."""
        self._data = data

    def invalidate(self):
        """Invalidate the cache."""
        self._data = None


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

    def get(self, identifier=None, by_id=False, filter_dict=None, **kwargs):
        """Return a flattened list of the data or a single entry by id if id is
        specified. Note that identifier is cleaned here, so don't clean in
        calling function.

        Any result other than None means that object was specifically added to
        the cache.

        Args:
            identifier: Specify an id to match to id_key. Returns a single
                dict.
        Keyword Args:
            by_id: A boolean of whether to return the results in a dict by
                id_key
            filter_dict: A dict to filter the return value on. If this is
                provided, only dicts that contain the items in filter_dict will
                be returned. Example: `{'classId': '12345'}`
        """
        if self._data is None:
            return None
        elif by_id is True:
            return _filter_dict(self._data, filter_dict) or None
        elif identifier:
            return self._data.get(qs.clean_id(identifier))
        else:
            return_list = qs.dict_to_dict_list(self._data)
            if self._sort_key:
                return_list = sorted(
                    return_list,
                    key=lambda x: x[self._sort_key])
            return _filter_list(return_list, filter_dict) or None

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

        if not self._data:
            self._data = {}
        cleaned_input = {qs.clean_id(i[self._id_key]): i for i in new_data}
        self._data.update(cleaned_input)

    def has_fields(self, fields):
        """Determine whether or not all of the cached data has all the fields
        specified.

        Returns False if self._data is none.
        """
        if str(fields) == fields:
            fields = [fields]
        elif type(fields) is not list:
            raise TypeError('Fields must be a list or string')
        if not self._data:
            return False

        for field in fields:
            if not all(field in d for k, d in self._data.iteritems()):
                return False
        return True

    def has_entry_with_subset(self, items):
        """Determine whether or not one of the entries in the cache has the
        items from items. Items should be in a dict, such as {id: 12345}.
        """
        for _, datum in self._data.iteritems():
            if _dict_has_subset(datum, items):
                return True
        return False


def _filter_dict(dict_to_filter, subset):
    """Filter dict_to_filter for items where the values contain the items in
    items.
    """
    if dict_to_filter is None or not subset:
        return dict_to_filter

    return {
        k: d for k, d in dict_to_filter.iteritems()
        if _dict_has_subset(d, subset)
    }


def _filter_list(list_to_filter, subset):
    """Filter list_to_filter for dicts that contain the items in items"""
    if list_to_filter is None or not subset:
        return list_to_filter

    return [
        i for i in list_to_filter
        if _dict_has_subset(i, subset)
    ]


def _dict_has_subset(dict_to_check, subset):
    """Boolean whether the dict contains the items in subset.

    It doesn't matter whether an item in subset is unicode or ascii string -
    they are compared as equal (both key and value).
    If subset is empty, True is returned.
    """
    if not subset: return True

    for k, v in subset.iteritems():
        if dict_to_check.get(k) is None:
            return False
        elif (dict_to_check[k] != v and str(dict_to_check[k]) != str(v)):
            return False
    return True
