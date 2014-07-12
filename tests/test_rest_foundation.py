"""Test the foundation for rest requests."""

import qs


def setup(module):
    global github
    qs.logger.silence()
    github = qs.GitHubRequest(
        'Test Request',
        '/users/{}/repos'.format('br1ckb0t'))
    github.make_request()


def test_request_success():
    assert github.successful is True


def test_content_is_correct():
    assert type(github.data) is list
    by_id = {i['id']: i for i in github.data}
    assert by_id[21495975]['name'] == 'QSTools'


def test_rate_limit_tracking_matches_request():
    server = qs.rate_limiting.get_server('github.com')
    assert server is not None
    rate_limit_header_field = qs.rate_limiting._GITHUB_LIMIT_HEADER
    github_remainaing = github.response.headers[rate_limit_header_field]
    assert server.remaining == github_remainaing


def test_merge():
    assert github._merge([{1: 1}, {2: 2}, {3: 3}]) == {1: 1, 2: 2, 3: 3}
