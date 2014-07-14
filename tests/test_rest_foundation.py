"""Test the foundation for rest requests."""

import qs
import config

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
    assert before_request_count == httpbin_server.request_count - 1
    assert before_response_count == httpbin_server.response_count - 1


def test_request_success():
    assert basic_get.successful is True


def test_content_is_correct():
    assert type(basic_get.data) is dict
    assert KEY in basic_get.data['args']
    assert basic_get.data['args'][KEY] == VAL


def test_rate_limit_tracking_matches_request():
    server = qs.rate_limiting.get_server('github')
    assert server is not None
    if github.successful:
        rate_limit_header_field = qs.rate_limiting._GITHUB_LIMIT_HEADER
        github_remaining = github.response.headers[rate_limit_header_field]
        assert server.remaining == github_remaining


def test_api_wrapper_init():
    wrapper = qs.APIWrapper(['qs', 'live', 'qstools'])
    assert wrapper.identifier == ['qs', 'live', 'qstools']
    assert wrapper.api_key == config.API_KEY


def test_request_repr():
    basic = qs.BaseRequest('do something', '/uri')
    assert '{}'.format(basic) == '<BaseRequest to do something at /uri>'
