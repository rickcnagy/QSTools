"""Test methods related to report cards"""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()


def test_get_report_cycles():
    assert_equals(len(q.get_report_cycles()), REPORT_CYCLE_COUNT)


def test_get_active_report_cycle():
    assert_true(q.get_active_report_cycle()['isActive'])


def test_get_report_card():
    rc = q.get_report_card(STUDENT_ID)
    assert_equals(rc['sectionLevel'][SECTION_WITH_GB]['marks'], MARKS)
