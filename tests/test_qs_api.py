"""Test the QS API wrapper from qs.qs_api"""

import qs
import config
from nose.tools import *


def test_make_request():
    request = qs.QSRequest('Testing', '/students')
    q = qs.API()
    q.make_request(request, {'critical': True})
    assert_equals(request.api_key, q.api_key)
    assert_in('apiKey', request.params)
    assert_equals(request.params['apiKey'], q.api_key)
    assert_true(request.critical)


def test_empty_access_key_arg():
    q = qs.API()
    assert_equals(q.schoolcode, 'qstools')
    assert_equals(q.api_key, config.API_KEY)


def test_api_key_as_access_key():
    q = qs.API(config.API_KEY)
    assert_equals(q.schoolcode, 'qstools')
    assert_equals(q.api_key, config.API_KEY)


def test_adding_api_key():
    fake_schoolcode = 'fakeschool'
    fake_api_key = '{}.fakeapikey'.format(fake_schoolcode)
    q = qs.API(fake_api_key)
    q.api_key = config.API_KEY
    q.get_students()
    assert_equals(q.schoolcode, fake_schoolcode)
    assert_equals(qs.api_keys.get(['qs', 'live', fake_schoolcode]),
        config.API_KEY)


def test_live():
    assert_true(qs.API().live)


def test_key_path():
    assert_equals(qs.API()._api_key_store_key_path(), ['qs', 'live', 'qstools'])
