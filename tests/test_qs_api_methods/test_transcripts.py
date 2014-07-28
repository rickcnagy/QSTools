"""Test methods related to Transcripts"""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()


def test_get_transcript():
    transcript = q.get_transcript(STUDENT_ID)
    assert_equals(transcript['sectionLevel'][SECTION_WITH_GB]['marks'], MARKS)
