#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Test the api_base module."""

import unittest
import qs

qs.logger.silence()


class GitHubRequest(qs.BaseRequest):
    base_url = 'https://api.github.com'


class GitHubRepoRequest(GitHubRequest):

    def __init__(self):
        super(GitHubRequest, self).__init__(
            'Test Request',
            '/users/{}/repos'.format('br1ckb0t'))


class TestBasicGet(unittest.TestCase):

    def setUp(self):
        self.request = self.GitHubRepoRequest()
        self.request.make_request()
        github_rate_limit_header = 'X-RateLimit-Remaining'
        self.limit_remaining = self.request.headers.get(github_rate_limit_header)

    def request_success(self):
        self.assertTrue(self.request.successful)

    def content_is_correct(self):
        by_id = {i['id']: i for i in self.request.data}
        self.assertTrue(by_id[21495975]['name'], 'QSTools')

    def headers_are_correct(self):
        self.assertIsInstance(self.limit_header_before, str)
        self.assertNotEqual(self.limit_header_before, '')

    def rate_limit_tracking_matches_request(self):
        server = rate_limiting.get_server('github.com')
        self.assertEqual(server.remaining, self.limit_remaining)

if __name__ == '__main__':
    unittest.main()
