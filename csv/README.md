CSV Scripts
===

####[`add_student_ids.py`](./add_student_ids.py)
Add a Student ID to each student row based on the First and Last or Full
Name columns.

If ignore_case is true, this will ignore case when matching student names
This doesn't save unless it finds matches for **all students in the csv**.

Usage: `./add_student_id {schoolcode} {filename.csv} {opt ignore_case} {opt enrolled_only}`

Requires: CSV with columns: *First* and *Last*, which are exact matches to the first name and last name of a student database.

Outputs: The same CSV, but with a "Student ID" column at the end.


###['add_section_ids.py'](./add_section_ids.py)
Get the section id (within the current active semester) for the class a student is enrolled in. 

Usage: `./add_section_id {schoolcode} {filename.csv}

Requires: CSV with student id (generally retrived with [`add_student_ids.py`](./add_student_ids.py)), and a section name. One row per student enrollment. Within QuickSchools, each student must be enrolled in each of the sections appearing on the CSV within the current active semester. 

Outputs: The same CSV, but with a "Section ID" column at the end. 


####[`separate_first_last.py`](./separate_first_last.py)

Extract the first and last names from a "Last, First" Full Name column.

Usage: `./separate_first_last {filename.csv} [{overwrite}]`
Params:
    filename: the filename
    overwrite: whether or not to overwrite the existing file. Defaults to
        False.

Requires: CSV with a column entitled "Full Name" where all the names are in "Last, First" or "First Last".

Outputs: The same CSV, but with "First" and "Last" columns added.

####[`logs/`](./logs)
