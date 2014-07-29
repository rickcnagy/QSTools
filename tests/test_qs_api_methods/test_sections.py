"""Test the /sections related qs.API methods"""


from nose.tools import *
import qs
from qs.test_data import *
from mock import MagicMock


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

def test_get_section():
    new = qs.API()
    assert_equals(new.get_section(SECTION_ID)['sectionName'], SECTION_NAME)
    assert_greater(len(new._section_cache.get()), 1)


#  =================
#  = Match Section =
#  =================

def test_match_by_name():
    match = q.match_section(SECTION_NAME)
    assert_is_dnd(match)


def test_match_id():
    match = q.match_section(NAS1_SECTION_ID, match_name=False)


def test_match_dict():
    match_dict = {
        'sectionName': 'Do Not Delete',
        'sectionCode': 'DND',
    }
    match = q.match_section(match_dict)


def test_multiple_match():
    matches = q.match_section(DUPLICATE_SECTION_NAME, allow_multiple=True)
    assert_is_instance(matches, list)
    assert_equals(len(matches), DUPLICATE_SECTION_COUNT)
    for section in matches:
        assert_equals(section['sectionName'], DUPLICATE_SECTION_NAME)
    qs.logger = MagicMock()
    matches = q.match_section(DUPLICATE_SECTION_NAME)
    assert_equals(qs.logger.error.call_count, 1)


def test_with_student_id():
    match = q.match_section(SECTION_NAME, student_id=STUDENT_ID)
    assert_is_dnd(match)


def test_prior_semester():
    match = q.match_section(
        NAS1_SECTION_NAME,
        target_semester_id=NAS1_SEMESTER_ID)
    assert_equals(match['id'], NAS1_SECTION_ID)


def test_with_student_id_and_prior_semester():
    match = q.match_section(
        NAS1_SECTION_ID,
        target_semester_id=NAS1_SEMESTER_ID,
        student_id=STUDENT_ID)
    assert_equals(match['id'], NAS1_SECTION_ID)


def test_no_match():
    qs.logger = MagicMock()
    assert_is_none(q.match_section('Some Non-Existent Section Name'))
    assert_equals(qs.logger.error.call_count, 1)
    q.match_section('Some Non-Existent Section Name', critical=True)
    assert_equals(qs.logger.critical.call_count, 1)


def test_bad_identifier():
    with assert_raises(TypeError):
        q.match_section(['12345'])


def assert_is_dnd(section):
    assert_is_not_none(section)
    assert_equals(section['id'], SECTION_ID)
