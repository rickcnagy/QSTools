# Rolling Enrollment Semester Migration

This migrates semesters for rolling enrollment schools.

3 steps:

1. `download.py`
    - Get list of all invalid grades for each section: `invalid_grades`
    - Get a list of all students without valid grades: `enrolled_no_valid_grades`
    - Outputs `rolling_migration.json`
1. `upload.py`
    - Enroll all the students in Q2 from `enrolled_no_valid_grades`
    - Import `invalid_grades` into Q2
1. `unenroll.py`
    - Unenroll `enrolled_no_valid_grades` students from Q1
