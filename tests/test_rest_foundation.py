"""Test the foundation for rest requests."""

import qs
import config
from nose.tools import *
from mock import MagicMock

# Random keys just for testing
KEY = '0zX4EX'
VAL = 'Ei5kWV'


def setup(module):
    global basic_get, github, before_request_count, before_response_count

    httpbin_server = qs.rate_limiting.get_server('httpbin')
    before_request_count = httpbin_server.request_count
    before_response_count = httpbin_server.response_count

    basic_get = qs.HTTPBinRequest('Test Request', '/get')
    basic_get.params = {KEY: VAL}
    basic_get.make_request()

    github = qs.GitHubRequest(
        'Test Request',
        '/users/{}/repos'.format('br1ckb0t'))
    github.make_request()


def test_request_count_in_rate_limit_server():
    httpbin_server = qs.rate_limiting.get_server('httpbin')
    assert_equals(before_request_count, httpbin_server.request_count - 1)
    assert_equals(before_response_count, httpbin_server.response_count - 1)


def test_rate_limit_with_valid_urls():
    qs_url = 'https://api.quickschools.com/sms/v1'
    backup_url = 'https://api.smartschoolcentral.com/sms/v1'
    httpbin_url = 'https://www.httpbin.org'
    github_url = 'https://api.github.com'
    match_dict = {
        qs.rate_limiting.get_server(qs_url): 'qs_live',
        qs.rate_limiting.get_server(backup_url): 'qs_backup',
        qs.rate_limiting.get_server(httpbin_url): 'httpbin',
        qs.rate_limiting.get_server(github_url): 'github',
    }
    for server, identifier in match_dict.iteritems():
        assert_equals(server.identifier, identifier)


def test_get_server_at_bad_url():
    bad_url = 'http://somerandomapi.com/nothing'
    qs.logger = MagicMock()
    qs.rate_limiting.get_server(bad_url)
    qs.logger.warning.assert_called_once_with(
        'Making request/response at unrecognized URL, so no '
        'rate limiting or request tracking is in place for', bad_url)


def test_request_success():
    assert_true(basic_get.successful)


def test_content_is_correct():
    assert_is_instance(basic_get.data, dict)
    assert_in(KEY, basic_get.data['args'])
    assert_equals(basic_get.data['args'][KEY], VAL)


def test_rate_limit_tracking_matches_request():
    server = qs.rate_limiting.get_server('github')
    assert_is_not_none(server)
    if github.successful:
        rate_limit_header_field = qs.rate_limiting._GITHUB_LIMIT_HEADER
        github_remaining = github.response.headers[rate_limit_header_field]
        assert_equals(server.remaining, github_remaining)


def test_api_wrapper_init():
    wrapper = qs.APIWrapper(['qs', 'live', 'qstools'])
    assert_equals(wrapper.identifier, ['qs', 'live', 'qstools'])
    assert_equals(wrapper.api_key, config.API_KEY)


def test_request_repr():
    basic = qs.RestRequest('do something', '/uri')
    assert_equals('{}'.format(basic), '<RestRequest do something at /uri>')
