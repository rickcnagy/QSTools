"""Test the rest_cache module."""

import qs
from nose.tools import *

unsorted = [{
    'id': 12345,
    'sort': 2,
}, {
    'id': 146,
    'sort': 1
}]
sorted_version = [{
    'id': 146,
    'sort': 1
}, {
    'id': 12345,
    'sort': 2,
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


def test_filtered_get():
    cache = qs.ListWithIDCache()
    cache.add(unsorted)
    assert_true(cache.get(filter_dict=unsorted[0]), unsorted[0])


def test_filter_get_by_id():
    cache = qs.ListWithIDCache()
    cache.add(unsorted)
    unsorted_by_id = {unsorted[0]['id']: unsorted[0]}
    assert_true(cache.get(filter_dict=unsorted[0], by_id=True), unsorted_by_id)
    assert_is_none(cache.get(filter_dict={'some key': 1234}))


def test_filter_with_unicode():
    cache = qs.ListWithIDCache()
    unicoded = {u'id': u'someval'}
    no_unicode = {'id': 'someval'}
    cache.add(unicoded)
    assert_equals(cache.get(), [unicoded])
    assert_equals(cache.get(filter_dict=no_unicode), [unicoded])


def test_entry_has_items():
    cache = qs.ListWithIDCache()
    cache.add(unsorted)
    assert_true(cache.has_entry_with_subset({'sort': 1}))
    assert_false(cache.has_entry_with_subset({'sort': '1000'}))
    assert_false(cache.has_entry_with_subset({'somekey': 5}))
