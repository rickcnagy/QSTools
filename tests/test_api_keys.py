"""Test the API keys module"""

from qs import api_keys
import qs
from nose.tools import *
import json

TEMP_STORE_PATH = "~/.apikeys_testing.json"


def setup():
    global api_key_store_path
    api_key_store_path = api_keys.KEY_STORE_PATH
    api_keys.KEY_STORE_PATH = TEMP_STORE_PATH


def test_generate_key():
    assert_equals(api_keys._generate_key(['1', '2']), '1:2')
    assert_equals(api_keys._generate_key('1'), '1')
    assert_equals(api_keys._generate_key('1:2'), '1:2')


def test_generate_key_with_wrong_type():
    with assert_raises(TypeError):
        api_keys._generate_key(1)


def test_remove_nonexistent_key():
    with assert_raises(KeyError):
        api_keys.remove(qs.rand_str())


def test_get_api_key():
    assert_equals(api_keys.get(['qs', 'live', 'qstools']), qs.mock_data.KEY)


def test_remove_api_key():
    key = qs.rand_str()
    val = qs.rand_str()
    api_keys.set(key, val)
    assert_in(key, api_keys._get_db())
    api_keys.remove(key)
    assert_not_in(key, api_keys._get_db())


def test_setting_with_bad_api_key():
    with assert_raises(ValueError):
        api_keys.set('12345', '')


def test_setting_with_bad_key():
    with assert_raises(ValueError):
        api_keys.set('', '12345')


def test_api_key_path_order():
    key_path = ['1', '2', '3']
    val = qs.rand_str()
    api_keys.set(key_path, val)
    assert_equals(api_keys.get(key_path), val)
    with assert_raises(KeyError):
        api_keys.get(['2', '1', '3'])


def test_get_api_key_with_bad_key():
    with assert_raises(KeyError):
        api_keys.get(qs.rand_str())


def test_set_api_key():
    key = qs.rand_str()
    val = qs.rand_str()
    api_keys.set(key, val)
    with open(api_keys._get_path()) as f:
        assert_equals(json.load(f)[key], val)


def test_api_key_with_key_path():
    key_path = [qs.rand_str(), qs.rand_str(), qs.rand_str()]
    val = qs.rand_str()
    api_keys.set(key_path, val)
    assert_equals(api_keys.get(key_path), val)


def test_api_key_with_str_key():
    key = qs.rand_str()
    val = qs.rand_str()
    api_keys.set(key, val)
    assert_equals(api_keys.get(key), val)


def teardown():
    api_keys.invalidate()
    assert_false(api_keys._db_exists())
    api_keys.KEY_STORE_PATH = api_key_store_path
