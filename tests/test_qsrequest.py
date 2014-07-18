"""Test any request wrappers from rest_request_wrappers"""

import qs
from nose.tools import *
from qs import QSRequest
from mock import MagicMock
from qs.mock_data import *

# just for testing correct param val...
_MAGIC_VAL = '1546'


def setup(module):
    global paged_list, single_object, flat_list
    qs.logger.silence()

    paged_list = QSRequest('Paged List Request', '/students')
    paged_list.params = {'itemsPerPage': 1}
    paged_list.set_api_key(API_KEY)
    paged_list.make_request()

    assert_equals(len(paged_list.data), 1)
    assert_in('id', paged_list.data[0])
    student_id = paged_list.data[0]['id']

    single_object = QSRequest(
        'Single Object',
        '/students/{}'.format(student_id))
    single_object.set_api_key(API_KEY)
    single_object.make_request()

    flat_list = QSRequest(
        'Flat List',
        '/semesters')
    flat_list.params = {'some_param': _MAGIC_VAL}
    flat_list.headers = {'some_header': _MAGIC_VAL}
    flat_list.set_api_key(API_KEY)
    flat_list.make_request()


def test_paged_list():
    assert_is_instance(paged_list.data, list)
    assert_is_instance(paged_list.data[0], dict)
    assert_equals(paged_list.return_type, 'Paged List')


def test_single_object():
    assert_is_instance(single_object.data, dict)
    assert_equals(single_object.return_type, 'Single Object')


def test_flat_list():
    assert_is_instance(flat_list.data, list)
    assert_is_instance(flat_list.data[0], dict)
    assert_equals(flat_list.return_type, 'Flat List')


def test_live_url():
    semesters_url = 'https://api.quickschools.com/sms/v1/semesters'
    assert_equals(flat_list._full_url(), semesters_url)


def test_backup_url():
    sem_backup_url = 'https://api.smartschoolcentral.com/sms/v1/semesters'
    backup_request = QSRequest('Testing', '/semesters', live=False)
    assert_equals(backup_request._full_url(), sem_backup_url)


def test_params():
    full_params = flat_list._full_params()
    assert_in('some_param', full_params)
    assert_equals(full_params['some_param'], _MAGIC_VAL)


def test_headers():
    full_headers = flat_list._full_headers()
    assert_in('some_header', full_headers)
    assert_equals(full_headers['some_header'], _MAGIC_VAL)


def test_weird_response():
    request = qs.QSRequest('Weirdo', '/students')
    request.set_api_key('qstools.053904ef-90c1-3f94-bc84-cc95168f4f20')

    other_request = qs.HTTPBinRequest('Other', '/get')
    other_request.make_request()

    request.successful = True
    request.response = other_request.response

    qs.logger = MagicMock()
    request._get_data()
    qs.logger.critical.assert_called_once_with(
        "Unrecognized response data type",
        request.response.json())

if __name__ == '__main__':
    unittest.main()
