API Scripts
===
`delete_assignments_from_sections.py`
---

Delete assignments with specified ids from the specified sections.
Put in all of the sections known and assignments known and the script will match them.
This has the advantage that the specific assignment-section mapping doesn't have to be known.

`clear_gradebook.py`
---
Clear the gradebook in all sections section_ids

`check_section_and_enrollment_match.py`
---
Check that SOURCE_SEMESTER matches the current semester in both enrollment and sections

`check_sections_match.py`
---
Check that all sections in source_semester have a match in the active semester

`fake_gradebooks.py`
---
Fills every assignment in every section with fake gradebook data - useful
for creating fake gradebook data for demo schools or support trial schools.

Gradebook Migration/
---
Migrate gradebook data between semesters
