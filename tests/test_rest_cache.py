"""Test the rest_cache module."""

import qs
from nose.tools import *

unsorted = [{
    'id': 12345,
    'sort': 02,
}, {
    'id': 146,
    'sort': 01
}]
sorted_version = [{
    'id': 146,
    'sort': 01
},{
    'id': 12345,
    'sort': 02,
}]


def test_rest_cache_class():
    cache = qs.RestCache()
    some_string = qs.rand_str()

    cache.add(some_string)
    assert_equals(cache.get(), some_string)

    cache.invalidate()
    assert_is_none(cache.get())


def test_list_with_id_cache_basics():
    cache = qs.ListWithIDCache()

    cache.add({'id': 12345})
    assert_equals(cache.get(), [{'id': 12345}])
    assert_equals(cache.get(12345), {'id': 12345})
    assert_equals(cache.get(by_id=True), {'12345': {'id': 12345}})

    cache.invalidate()
    assert_is_none(cache.get(), None)


def test_get_by_id_with_bad_id():
    cache = qs.ListWithIDCache()
    cache.add({'id': 1})
    assert_is_none(cache.get(2))


def test_list_with_id_cache_sorting():
    cache = qs.ListWithIDCache(sort_key='sort')
    cache.add(unsorted)
    assert_equals(cache.get(), sorted_version)

def test_list_with_id_cache_validation():
    cache = qs.ListWithIDCache()
    with assert_raises(TypeError):
        cache.add("this will error, since it's a string")
    with assert_raises(TypeError):
        cache.add(["this too, since it's a string, not a dict, in a list"])


def test_has_fields():
    cache = qs.ListWithIDCache()
    with assert_raises(TypeError):
        cache.has_fields(123)
    cache.add(unsorted)
    assert_true(cache.has_fields(['sort', 'id']))
    assert_true(cache.has_fields('sort'))
    assert_false(cache.has_fields(['sort', 'some random field']))
