"""Test the QS API wrapper from qs.qs_api"""

import qs
import config


def test_qs_api_with_api_key_as_access_key():
    q = qs.API(config.API_KEY)
    assert q.schoolcode == 'qstools'
    assert q.api_key == config.API_KEY
