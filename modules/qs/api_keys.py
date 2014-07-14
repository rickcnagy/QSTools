#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Module for setting and getting API keys in the locally saved API key store,
which is stored in ~/API keys.json
"""

import json
import qs
import os

KEY_STORE_PATH = '~/.apikeys.json'
SAMPLE_API_KEY_STORE = {
    "qs:live:qstools": "qstools.053904ef-90c1-3f94-bc84-cc95168f4f20"
}


def set(key, api_key):
    """Set the key/api_key in the API key store.

    Args:
        key: a key (or keys) to store the api_key under. If it's a list of
            keys, the value will be stored colon-delimeted and can be accessed
            by passing the same list of keys to get()
        api_key: the value to store
    """
    if api_key:
        db = _get_db()
        db_key = _generate_key(key)
        db[db_key] = api_key
        _save_db(db)
    else:
        raise ValueError("'{}' isn't a valid API key".format(api_key))


def get(key):
    """Get the matching api_key for key in the API key store.

    Args:
        key: a key (or keys) to access the api_key from. If it's a list of
            keys, only a value that were stored with all values in the list
            will be returned.
    """
    db = _get_db()
    db_key = _generate_key(key)
    if db_key in db:
        return db[db_key]
    else:
        raise KeyError("{} isn't a key in the API key store.".format(key))


def remove(key):
    """Remove a key from the key store"""
    db = _get_db()
    db_key = _generate_key(key)
    if db_key in db:
        del db[db_key]
        _save_db(db)
        print "Removed {} from the API key store".format(db_key)
    else:
        raise KeyError("{} isn't a key in the API key store.".format(key))


def _generate_key(str_or_list_key):
    keys = []
    if not str_or_list_key:
        raise ValueError("Key is {}, must equate to True".format(
            str_or_list_key))
    if type(str_or_list_key) is str:
        keys = [str_or_list_key]
    elif type(str_or_list_key) is list:
        keys = str_or_list_key
    else:
        raise TypeError("Key is {}, should be string or list".format(
            type(str_or_list_key)))
    return ':'.join(keys)


def _get_path():
    """Return the path of the key store"""
    return os.path.expanduser(KEY_STORE_PATH)


def _get_db():
    """Open and return the entire API key db. If the db isn't found,
    _create_db() is called
    """
    _create_db_if_necessary()
    with open(_get_path()) as f:
        return json.load(f)


def _save_db(db):
    """Save the db to disk. Just as in _get_db(), if the db isn't found,
    _create_db() is called firstrna
    """
    _create_db_if_necessary()
    with open(_get_path(), 'w') as f:
        json.dump(db, f, indent=4, sort_keys=True)


def _create_db_if_necessary():
    """Create the db on disk by copying from SAMPLE_API_KEY_STORE
    """
    if not _db_exists():
        with open(_get_path(), 'w') as f:
            json.dump(SAMPLE_API_KEY_STORE, f)
            return


def _db_exists():
    """Determine whether the db exists at KEY_STORE_PATH"""
    return os.path.isfile(_get_path())


def _clear_db():
    os.remove(_get_path())
