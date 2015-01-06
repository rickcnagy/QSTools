"""Test the QS API wrapper from qs.qs_api"""

import qs
from nose.tools import *
from mock import MagicMock
from qs.test_data import *


def setup():
    global q
    q = qs.API()


def test_make_request():
    request = qs.QSRequest('Testing', '/students')
    q = qs.API()
    data = q._make_request(request, critical=True)
    assert_is_instance(data, list)
    assert_equals(request.api_key, q.api_key)
    assert_in('apiKey', request.params)
    assert_equals(request.params['apiKey'], q.api_key)
    assert_true(request.critical)


def test_empty_access_key_arg():
    q = qs.API()
    assert_equals(q.schoolcode, 'qstools')
    assert_equals(q.api_key, API_KEY)


def test_api_key_as_access_key():
    q = qs.API(API_KEY)
    assert_equals(q.schoolcode, 'qstools')
    assert_equals(q.api_key, API_KEY)


def test_adding_api_key():
    fake_schoolcode = 'fakeschool'
    fake_api_key = '{}.fakeapikey'.format(fake_schoolcode)
    q = qs.API(fake_api_key)
    q.api_key = API_KEY
    q.get_students()
    if q.get_students():
        assert_equals(q.schoolcode, fake_schoolcode)
        assert_equals(qs.api_keys.get(['qs', 'live', fake_schoolcode]),
            API_KEY)
        qs.api_keys.remove(['qs', 'live', 'fakeschool'])


def test_live():
    assert_equals(qs.API().server, 'live')


def test_key_path():
    assert_equals(
        qs.API()._api_key_store_key_path(),
        ['qs', 'live', 'qstools'])


def test_make_request_with_fields():
    request_with_field('deleted')
    request_with_field('hasLeft')


def request_with_field(field):
    data = q.get_students(fields=field)
    assert_true(all(field in i for i in data))
    assert_false(data[0][field])
    assert_true(all(field in i for i in q.get_students()))


def test_make_request_no_cache():
    students = q.get_students(fields='deleted')
    assert_true(all('deleted' in i for i in students))
    assert_false(any('deleted' in i for i in q.get_students(use_cache=False)))
