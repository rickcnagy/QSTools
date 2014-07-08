#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Test that all is well with the api_base class."""

import unittest
import api_base
import api_logging


class TestBasicGet(unittest.TestCase):
    api_logging.silent = True

    class TestRequest(api_base.BaseRequest):
        base_url = 'https://api.github.com'

    def setUp(self):
        self.request = self.TestRequest('Test Request', '/users/{}/repos'.format('br1ckb0t'))
        self.request.make_request()

    def test_success(self):
        self.assertTrue(self.request.successful)

if __name__ == '__main__':
    unittest.main()
