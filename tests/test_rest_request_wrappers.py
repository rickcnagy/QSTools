#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Test any request wrappers from rest_request_wrappers"""

import unittest
import qs
import config

# just for testing correct param val...
_MAGIC_VAL = '1546'


class TestQSRequest(unittest.TestCase):

    def setUp(self):
        qs.logger.silence()
        self.paged_list = qs.QSRequest('Paged List Request', '/students')
        self.paged_list.params = {'itemsPerPage': 1}
        self.paged_list.set_api_key(config.API_KEY)
        self.paged_list.make_request()

        self.assertEquals(len(self.paged_list.data), 1)
        self.assertIn('id', self.paged_list.data[0])
        student_id = self.paged_list.data[0]['id']

        self.single_object = qs.QSRequest(
            'Single Object',
            '/students/{}'.format(student_id))
        self.single_object.set_api_key(config.API_KEY)
        self.single_object.make_request()

        self.flat_list = qs.QSRequest(
            'Flat List',
            '/semesters')
        self.flat_list.params = {'some_param': _MAGIC_VAL}
        self.flat_list.headers = {'some_header': _MAGIC_VAL}
        self.flat_list.set_api_key(config.API_KEY)
        self.flat_list.make_request()

    def test_paged_list(self):
        self.assertIsInstance(self.paged_list.data, list)
        self.assertIsInstance(self.paged_list.data[0], dict)

    def test_single_object(self):
        self.assertIsInstance(self.single_object.data, dict)

    def test_flat_list(self):
        self.assertIsInstance(self.flat_list.data, list)
        self.assertIsInstance(self.flat_list.data[0], dict)

    def test_qs_live_request_url(self):
        semesters_url = 'https://api.quickschools.com/sms/v1/semesters'
        self.assertEquals(self.flat_list._full_url(), semesters_url)

    def test_qs_params(self):
        full_params = self.flat_list._full_params()
        self.assertIn('some_param', full_params)
        self.assertEquals(full_params['some_param'], _MAGIC_VAL)

    def test_qs_headers(self):
        full_headers = self.flat_list._full_headers()
        self.assertIn('some_header', full_headers)
        self.assertEquals(full_headers['some_header'], _MAGIC_VAL)


if __name__ == '__main__':
    unittest.main()
