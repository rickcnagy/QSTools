API Scripts
===

This directory is for scripts that manipulate data on a school's account using the API. In general, scripts' usuage is something like:

`./some_script.py {schoolcode} {other-params} {csv-filename.csv}`

As a note about the schoolcode param: this stands in for the API key for a school. You can always enter the API key in directly or you may switch to using just the school code after you have run a script using the full API key in this param once. Your API keys are saved to a `.apiKeys.json` file in your home directory after you use the API key once. Check out ['api_keys.py'](./modules/qs/api_keys.py) for how this works.

Scripts
___

Individual, general purpose scripts are listed in the main directory here. Check out the info and the docstring on the script itself to see the details and usage.

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

CLI usage:
./copy_enrollments_from_backup_server.py {schoolcode}


####[`delete_all_assignments.py`](./delete_all_assignments.py)

Delete ALL assignments, including final grades, for ALL sections in the
active semester

Be VERY careful with this one.

CLI Usage:
./delete_all_assignments {schoolcode}


####[`delete_all_section_enrollments.py`](./delete_all_section_enrollments.py)

Unenroll all students from all sections in the active semester.

CLI usage:

./delete_all_section_enrollments.py {schoolcode}


####[`delete_all_sections.py`](./delete_all_sections.py)


DELETE all sections.

For now, requires enrollment to be 0 for all sections - otherwise, QS throws
a soft error.

Usage:
./delete_all_sections {schoolcode} {server}


####[`delete_assignments_from_sections.py`](./delete_assignments_from_sections.py)

Delete assignments with specified ids from the specified sections.
Put in all of the sections known and assignments known and the script will match them.
This has the advantage that the specific assignment-section mapping doesn't have to be known.


####[`fake_gradebooks.py`](./fake_gradebooks.py)


Fills every assignment in every section with fake gradebook data - useful
for creating fake gradebook data for demo schools or support trial schools.

####[`import_attendance.py`](./import_attendance.py)

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


####[`import_fees.py`](./import_fees.py)

Import fees for each student from a CSV. Imports 1 fee per row.


The CSV should have the following columns:
- Student ID
- Amount
- Date
- Description

Command line usage:
./import_fees {CSV filename} {schoolcode}

Procedures
___

More complex, and repetitve, processes are grouped into subdirectories in the Procedures directory. In general, these collections of scripts are generally common requests that require little to no customization. 

####[`Report Card Grades to Transcripts/`](./procedures/Report Card Grades to Transcripts)

####[`Gradebook Migration/`](./procedures/Gradebook Migration)

####[`Rolling Enrollment Semester Migration/`](./procedures/Rolling Enrollment Semester Migration)

Logging
___
####[`logs/`](./logs)

Since we're working with live data in a production setting, it's really important to keep good logs. Each of the subdirectories of the repo have a space for logs (these are not tracked with git). Check out [**qs_logger**](../modules/qs/logger.py) for more about that. 
