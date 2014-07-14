"""Test the QS API wrapper from qs.qs_api"""

import qs
import config


def test_api_key_as_access_key():
    q = qs.API(config.API_KEY)
    assert q.schoolcode == 'qstools'
    assert q.api_key == config.API_KEY


def test_adding_api_key():
    fake_schoolcode = 'fakeschool'
    fake_api_key = '{}.fakeapikey'.format(fake_schoolcode)
    q = qs.API(fake_api_key)
    assert q.schoolcode == fake_schoolcode
    assert q.api_key == fake_api_key
    assert qs.api_keys.get(['qs', 'live', fake_schoolcode]) == fake_api_key


def test_api_key_lookup():
    q = qs.API('qstools')
    assert q.schoolcode == 'qstools'
    assert q.api_key == config.API_KEY


def test_live():
    assert qs.API('qstools').live is True
