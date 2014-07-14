"""Test the API keys module"""

from qs import api_keys
import qs
from nose.tools import raises
import json
import config

TEMP_STORE_PATH = "~/.apikeys_testing.json"


def setup():
    global api_key_store_path
    api_key_store_path = api_keys.KEY_STORE_PATH
    api_keys.KEY_STORE_PATH = TEMP_STORE_PATH


def test_generate_key():
    assert api_keys._generate_key(['1', '2']) == '1:2'
    assert api_keys._generate_key('1') == '1'
    assert api_keys._generate_key('1:2') == '1:2'


@raises(TypeError)
def test_generate_key_with_wrong_type():
    api_keys._generate_key(1)


@raises(KeyError)
def test_remove_nonexistent_key():
    api_keys.remove(qs.rand_str())


def test_get_api_key():
    assert api_keys.get(['qs', 'live', 'qstools']) == config.API_KEY


def test_remove_api_key():
    key = qs.rand_str()
    val = qs.rand_str()
    api_keys.set(key, val)
    assert key in api_keys._get_db()
    api_keys.remove(key)
    assert key not in api_keys._get_db()


@raises(ValueError)
def test_setting_with_bad_api_key():
    api_keys.set('12345', '')


@raises(ValueError)
def test_setting_with_bad_key():
    api_keys.set('', '12345')


@raises(KeyError)
def test_api_key_path_order():
    key_path = ['1', '2', '3']
    val = qs.rand_str()
    api_keys.set(key_path, val)
    assert api_keys.get(key_path) == val
    api_keys.get(['2', '1', '3'])


@raises(KeyError)
def test_get_api_key_with_bad_key():
    api_keys.get(qs.rand_str())


def test_set_api_key():
    key = qs.rand_str()
    val = qs.rand_str()
    api_keys.set(key, val)
    with open(api_keys._get_path()) as f:
        assert json.load(f)[key] == val


def test_api_key_with_key_path():
    key_path = [qs.rand_str(), qs.rand_str(), qs.rand_str()]
    val = qs.rand_str()
    api_keys.set(key_path, val)
    assert api_keys.get(key_path) == val


def test_api_key_with_str_key():
    key = qs.rand_str()
    val = qs.rand_str()
    api_keys.set(key, val)
    assert api_keys.get(key) == val


def teardown():
    api_keys._clear_db()
    assert not api_keys._db_exists()
    api_keys.KEY_STORE_PATH = api_key_store_path
