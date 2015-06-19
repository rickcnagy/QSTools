API Scripts
===

This directory is for scripts that manipulate data on a school's account using the API. In general, scripts' usuage is something like:

`./some_script.py {schoolcode} {other-params} {csv-filename.csv}`

As a note about the schoolcode param: this stands in for the API key for a school. You can always enter the API key in directly or you may switch to using just the school code after you have run a script using the full API key in this param once. Your API keys are saved to a `.apiKeys.json` file in your home directory after you use the API key once. Check out ['api_keys.py'](./modules/qs/api_keys.py) for how this works.

##[`Attendance`](./attendance)

####[`import_attendance.py`](./attendance/import_attendance.py)

Import attendance records from a CSV.

Required Columns:
    Student ID
    Teacher ID
    Date
    Status
    Remarks
    Description

Command Line Usage:
    ./import_attendance {filename} {schoolcode}



##[`Enrollments`](./enrollments)

####[`compare_two_semesters_section_enrollments.py`](./enrollments/compare_two_semesters_section_enrollments.py)
Checks for discrepancies between enrollments for two specified semesters by comparing enrollments by section id

Usage:
./compare_two_semesters_section_ernrollments.py schoolcode sect1_id sect2_id

####[`copy_enrollments_from_backup_server.py`](./enrollments/copy_enrollments_from_backup_server.py)
Copy subject enrollment from all subjects on the backup server to live.

Run with Q1 active on live and backup

CLI usage:
./copy_enrollments_from_backup_server.py {schoolcode}

####[`delete_all_section_enrollments.py`](./enrollments/delete_all_section_enrollments.py)
Unenroll all students from all sections in the active semester.

CLI usage:

./delete_all_section_enrollments.py {schoolcode}

####[`enroll_in_existing_sections`](./enrollments/enroll_in_existing_sections.py)
Enrolls students in sections that have already been created.

Requires: CSV of enrollment data with subject codes, semester id.
CSV must have the following columns: Student ID, Section Code

Usage: ./enroll_in_existing_sections.py {school code} {semester} filename.csv



##[`Fees`](./fees)

####[`import_fees.py`](./fees/import_fees.py)

Import fees for each student from a CSV. Imports 1 fee per row.


The CSV should have the following columns:
- Student ID
- Amount
- Date
- Description

Command line usage:
./import_fees {CSV filename} {schoolcode}



##[`Grades & Assignments`](./grades-assignments)

####[`clear_gradebook.py`](./grades-assignments/clear_gradebook.py)

Clear the gradebook in all sections section_ids

####[`delete_all_assignments.py`](./grades-assignments/delete_all_assignments.py)

Delete ALL assignments, including final grades, for ALL sections in the
active semester

Be VERY careful with this one.

CLI Usage:
./delete_all_assignments {schoolcode}

####[`delete_all_section_enrollments.py`](./grades-assignments/delete_all_section_enrollments.py)

Unenroll all students from all sections in the active semester.

CLI usage:

./delete_all_section_enrollments.py {schoolcode}

####[`delete_assignments_from_sections.py`](./grades-assignments/delete_assignments_from_sections.py)

Delete assignments with specified ids from the specified sections.
Put in all of the sections known and assignments known and the script will match them.
This has the advantage that the specific assignment-section mapping doesn't have to be known.

####[`fake_gradebooks.py`](./grades-assignments/fake_gradebooks.py)
Fills every assignment in every section with fake gradebook data - useful
for creating fake gradebook data for demo schools or support trial schools.



##[`Procedures`](./procedures)
Contains fairly standard multistep processes. In general, these are for migrating data within QS, not from an outside system.

####[`Report Card Grades to Transcripts/`](./procedures/Report Card Grades to Transcripts)
Moves data from Report Cards to transcripts (for example, for manually entered grades)

####[`Gradebook Migration/`](./procedures/Gradebook Migration)
Migrates data between semesters (for example, if a school makes a new semester after teachers have begun grading for it)



##[`Report Cards`](./report-card)

####[`import_rc_section_level.py`](./report-card/import_rc_section_level.py)

Import report card data at the section level.

Combines things so no more than one POST per student.

Uses the current report cycle.

Will soft error if an entry fails (error but not exit).

Takes a CSV with the following format:
+------------+------------+--------------+-------+
| Student ID | Section ID |  Identifier  | Value |
+------------+------------+--------------+-------+
|     252251 |     669067 | marks        | 110   |
|     252251 |     669067 | letter-grade | A++   |
+------------+------------+--------------+-------+


See examples/import_section_level.example.csv for an example import file.

CLI Usage:
python import_section_level.py {schoolcode} {csv_filename}



##[`Sections`](./sections)
This subdirectory is for scripts that manipulate sections, but not thier enrollments. 

####[`check_section_name_match.py`](./check_section_name_match.py)
Check that all sections in a term have a match by name in the other term.
Useful for Zeus related scripts.

####[`check_sections_match_exactly.py`](./check_sections_match_exactly.py)
Check that all sections in source_semester have an exact match in the active semester

####[`delete_all_sections.py`](./delete_all_sections.py)
DELETE all sections.

For now, requires enrollment to be 0 for all sections - otherwise, QS throws
a soft error.

Usage:
./delete_all_sections {schoolcode} {server}

