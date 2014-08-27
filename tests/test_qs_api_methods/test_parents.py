"""Tests related to parents"""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()
    q.get_parents()


def test_get_parents():
    parents = q.get_parents(by_id=True)
    assert_equals(parents[PARENT_ID]['fullName'], PARENT_NAME)


def test_get_parent():
    parent = q.get_parent(PARENT_ID)
    assert_equals(parent['fullName'], PARENT_NAME)
