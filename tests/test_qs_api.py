"""Test the QS API wrapper from qs.qs_api"""

import qs
from nose.tools import *
from mock import MagicMock
from qs.qs_api import _clean_id


def test_make_request():
    request = qs.QSRequest('Testing', '/students')
    q = qs.API()
    data = q.make_request(request, {'critical': True})
    assert_is_instance(data, list)
    assert_equals(request.api_key, q.api_key)
    assert_in('apiKey', request.params)
    assert_equals(request.params['apiKey'], q.api_key)
    assert_true(request.critical)


def test_empty_access_key_arg():
    q = qs.API()
    assert_equals(q.schoolcode, 'qstools')
    assert_equals(q.api_key, qs.mock_data.KEY)


def test_api_key_as_access_key():
    q = qs.API(qs.mock_data.KEY)
    assert_equals(q.schoolcode, 'qstools')
    assert_equals(q.api_key, qs.mock_data.KEY)


def test_adding_api_key():
    fake_schoolcode = 'fakeschool'
    fake_api_key = '{}.fakeapikey'.format(fake_schoolcode)
    q = qs.API(fake_api_key)
    q.api_key = qs.mock_data.KEY
    q.get_students()
    assert_equals(q.schoolcode, fake_schoolcode)
    assert_equals(qs.api_keys.get(['qs', 'live', fake_schoolcode]),
        qs.mock_data.KEY)
    qs.api_keys.remove(['qs', 'live', 'fakeschool'])


def test_live():
    assert_true(qs.API().live)


def test_key_path():
    assert_equals(qs.API()._api_key_store_key_path(), ['qs', 'live', 'qstools'])


def test_clean_id():
    value_errors = [None, {}, '']
    for error in value_errors:
        with assert_raises(ValueError):
            _clean_id(error)

    type_errors = [45.6, ['SomeID']]
    for error in type_errors:
        with assert_raises(TypeError):
            _clean_id(error)

    good_inputs = [1234, u'1234', '1234', '1g5H6', 0]
    for good_input in good_inputs:
        assert_equals(str(good_input), _clean_id(good_input))
