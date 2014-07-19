"""Test the get_semesters() method"""

import qs
from nose.tools import *
from qs.test_data import *


def setup(module):
    global q
    q = qs.API()
    q.get_semesters()

# ====================
# = .get_semesters() =
# ====================

def test_get_semesters():
    semesters = q.get_semesters()
    assert_is_instance(semesters, list)
    assert_greater(len(semesters), 0)


def test_get_semesters_by_id():
    assert_is_instance(q.get_semesters(by_id=True), dict)


def test_get_semesters_content():
    assert_equals(
        q.get_semesters(by_id=True)[ACTIVE_SEMESTER_ID]['semesterName'],
        ACTIVE_SEMESTER_NAME)


# ===================
# = .get_semester() =
# ===================

def test_get_semester():
    assert_equals(
        q.get_semesters(by_id=True)[ACTIVE_SEMESTER_ID],
        q.get_semester(ACTIVE_SEMESTER_ID))

# ==========================
# = .get_active_semester() =
# ==========================

def test_get_active_semester():
    assert_is_instance(q.get_active_semester(), dict)
    assert_true(q.get_active_semester()['isActive'])


# ======================
# = .get_active_year_id =
# ======================

def test_get_active_year_id():
    assert_equals(q.get_active_semester()['yearId'], q.get_active_year_id())


# ============================
# = .get_semesters_from_year =
# ============================

def test_get_semesters_from_year():
    semester_ids = [
        i['id'] for i
        in q.get_semesters_from_year(NA_YEAR_ID)
    ]
    assert_equals(set(semester_ids), set(NA_YEAR_SEMESTER_IDS))
