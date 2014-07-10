#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Test the api_base module."""

import unittest
import qs


class TestBasicGet(unittest.TestCase):

    class TestRequest(qs.BaseRequest):
        base_url = 'https://api.github.com'

    def setUp(self):
        qs.logger.silence()
        self.request = self.TestRequest(
            'Test Request',
            '/users/{}/repos'.format('br1ckb0t'))
        self.request.make_request()

    def test_request_success(self):
        self.assertTrue(self.request.successful)

    def test_content_is_correct(self):
        by_id = {i['id']: i for i in self.request.data}
        self.assertTrue(by_id[21495975]['name'], 'QSTools')

if __name__ == '__main__':
    unittest.main()