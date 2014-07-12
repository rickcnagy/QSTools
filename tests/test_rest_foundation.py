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
        self.github = GitHubRepoRequest()
        self.github.make_request()

    def test_request_success(self):
        self.assertTrue(self.github.successful)

    def test_content_is_correct(self):
        self.assertIsInstance(self.github.data, list)
        by_id = {i['id']: i for i in self.github.data}
        self.assertEqual(by_id[21495975]['name'], 'QSTools')

    def test_rate_limit_tracking_matches_request(self):
        server = qs.rate_limiting.get_server('github.com')
        self.assertIsNotNone(server.remaining)
        self.assertEqual(
            server.remaining,
            self.github.response.headers[qs.rate_limiting._GITHUB_LIMIT_HEADER])

if __name__ == '__main__':
    unittest.main()
