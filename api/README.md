API Scripts
===

####`check_section_and_enrollment_match.py`

Check that SOURCE_SEMESTER matches the current semester in both enrollment and sections.

####`check_section_name_match.py`

Check that all sections in a term have a match by name in the other term.
Useful for Zeus related scripts.


####`check_sections_match_exactly.py`

Check that all sections in source_semester have an exact match in the active semester

####`clear_gradebook.py`

Clear the gradebook in all sections section_ids

####`delete_assignments_from_sections.py`

Delete assignments with specified ids from the specified sections.
Put in all of the sections known and assignments known and the script will match them.
This has the advantage that the specific assignment-section mapping doesn't have to be known.


####`fake_gradebooks.py`


Fills every assignment in every section with fake gradebook data - useful
for creating fake gradebook data for demo schools or support trial schools.


####`student_name_to_id_matcher.py`

Take a CSV with student names and add a student ID column with Student IDs matched by name