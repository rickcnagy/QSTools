"""Test the API Keys module"""

from qs import api_keys
from nose.tools import raises
import random

TEMP_STORE_PATH = "~/API Keys Testing.json"


def setup(module):
    global api_key_store_path
    api_key_store_path = api_keys.KEY_STORE_PATH
    api_keys.KEY_STORE_PATH = TEMP_STORE_PATH


def test_generate_key():
    assert api_keys._generate_key(['1', '2']) == '1:2'
    assert api_keys._generate_key('1') == '1'
    assert api_keys._generate_key('1:2') == '1:2'


@raises(TypeError)
def test_generate_key_with_wrong_type():
    _generate_key(1)


def test_get_api_key():
    assert api_keys.get(['qs', 'live', 'qstools']) == config.API_KEY


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
    with open(TEMP_STORE_PATH) as f:
        assert json.loads(f)[key] == val


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


def teardown(module):
    api_keys.KEY_STORE_PATH = api_key_store_path
