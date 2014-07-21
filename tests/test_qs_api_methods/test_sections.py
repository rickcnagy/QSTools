"""Test the /sections related qs.API methods"""


from nose.tools import *
import qs
from qs.test_data import *

def setup():
    global q
    q = qs.API()
    q.get_sections()


def test_get_sections():
    sections = q.get_sections()

    assert_is_instance(sections, list)
    assert_greater(len(sections), 0)
    assert_is_instance(sections[0], dict)
    assert_in('id', sections[0])


def test_get_section_by_id():
    by_id = q.get_sections(by_id=True)
    assert_equals(by_id[SECTION_ID]['sectionName'], SECTION_NAME)


def test_get_sections_from_other_semester():
    other = q.get_sections(semester_id=NAS1_SEMESTER_ID)
    assert_is_instance(other, list)
    assert_equals(len(other), NAS1_SECTION_COUNT)


def test_get_sections_from_other_by_id():
    other = q.get_sections(semester_id=NAS1_SEMESTER_ID, by_id=True)
    assert_is_instance(other, dict)
    assert_not_equal(other, q.get_sections(by_id=True))
    other_name = other[NAS1_SECTION_ID]['sectionName']
    assert_equals(other_name, NAS1_SECTION_NAME)


def test_active_only():
    q.get_sections(semester_id=NAS1_SEMESTER_ID)
    assert_not_in(NAS1_SECTION_ID, q.get_sections(by_id=True))
    assert_in(NAS1_SECTION_ID, q.get_sections(by_id=True, active_only=False))

def test_get_all():
    all_sections = q.get_sections(by_id=True, all_semesters=True)
    assert_in(NAS2_SECTION_ID, all_sections)
    assert_in(NAS1_SECTION_ID, all_sections)
    assert_in(SECTION_ID, all_sections)
