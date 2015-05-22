API Scripts
===

This directory contains all the scripts used for changing data on QuickSchools. Subdirectories here are 
collections of scripts - generally for specific kinds of imports. 

**Calling Scripts**
While each script defines its own input args, the CLI usage is:
`schoolcode server filename other inputs`
Many (of the more stable) scripts have comments or documenation outlying the exact syntax.

Contents
----
####[`check_section_and_enrollment_match.py`](./check_section_and_enrollment_match.py)
Check that SOURCE_SEMESTER matches the current semester in both enrollment and sections.

####[`check_section_name_match.py`](./check_section_name_match.py)
Check that all sections in a term have a match by name in the other term.
Useful for Zeus related scripts.

####[`check_sections_match_exactly.py`](./check_sections_match_exactly.py)
Check that all sections in source_semester have an exact match in the active semester

####[`clear_gradebook.py`](./clear_gradebook.py)
Clear the gradebook in all sections section_ids

####[`copy_enrollments_from_backup_server.py`](./copy_enrollments_from_backup_server.py)
Copy subject enrollment from all subjects on the backup server to live.

Run with Q1 active on live and backup


####[`delete_all_assignments.py`](./delete_all_assignments.py)
Delete ALL assignments, including final grades, for ALL sections in the
active semester

Be VERY careful with this one. Runs on LIVE only. 


####[`delete_all_section_enrollments.py`](./delete_all_section_enrollments.py)
Unenroll all students from all sections in the active semester.


####[`delete_all_sections.py`](./delete_all_sections.py)
DELETE all sections.
For now, requires enrollment to be 0 for all sections - otherwise, QS throws
a soft error.


####[`delete_assignments_from_sections.py`](./delete_assignments_from_sections.py)
DELETE assignments with specified ids from the specified sections.
Put in all of the sections known and assignments known and the script will match them.
This has the advantage that the specific assignment-section mapping doesn't have to be known.


####[`fake_gradebooks.py`](./fake_gradebooks.py)
Fills every assignment in every section with fake gradebook data - useful
for creating fake gradebook data for demo schools or support trial schools.

####[`import_attendance.py`](./import_attendance.py)
Import attendance records from a CSV.
Required Columns:
- Student ID
- Teacher ID
- Date
- Status
- Remarks
- Description
Command Line Usage: `./import_attendance {filename} {schoolcode}`

####[`import_fees.py`](./import_fees.py)
Import fees for each student from a CSV. Imports 1 fee per row.
The CSV should have the following columns:
- Student ID
- Amount
- Date
- Description
Command line usage: `./import_fees {CSV filename} {schoolcode}`

####[`logs/`](./logs)
All scripts are required to log.

####[`Report Card Grades to Transcripts/`](./Report Card Grades to Transcripts)
Procedure for move grades from Report Cards to transcripts, if they have been entered manually. 

####[`Rolling Enrollment Semester Migration/`](./Rolling Enrollment Semester Migration)
Developed for individualized learning schools that utilize rolling enrollment setups, this procedue is structured for moving students grades from one semester to another, if they have not yet completed their coursework (i.e. had a final grade entered). A date is set for the academic year cutoff date. If students' work is complete, it is left in the 'old' semester, and if it is incomplete, it is moved to the 'new' semester. 