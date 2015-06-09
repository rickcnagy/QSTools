# Rolling Enrollment Semester Migration

This migrates semesters for rolling enrollment schools.

Note that a *valid grade* = stay in Q1

If a student has some assignments valid in Q1 but not all, upload.py will
dusplay a warning. In that case, the student will be left in Q1 and you should
do the migration for that student/section by hand.

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


Full usage:
```
./download.py {schoolcode} # Q1 Active
./upload.py {schoolcode} # Q2 Active
./unenroll.py {schoolcode} # Q1 Active
```
