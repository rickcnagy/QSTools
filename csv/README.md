CSV Scripts
===

####[`add_student_ids.py`](./add_student_ids.py)

Add a Student ID to each student row based on the First and Last columns.

Usage:
    ./add_student_id {filename.csv} {schoolcode}

Requires:
    A CSV with "First" and "Last" columns, with an exact name match to the
        provided school database for each student.

Outputs:
    The same CSV, but with a "Student ID" column.


####[`separate_first_last.py`](./separate_first_last.py)

Extract the first and last names from a "Last, First" Full Name column.

Usage:
    ./separate_first_last {filename.csv}

Requires:
    A column entitled "Full Name" where all the names are in "Last, First"

Outputs:
    The same CSV, but with "First" and "Last" columns added.