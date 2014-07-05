Gradebook Migration
===
Migrate gradebook data between semesters

Directions
---
(Q1 is old semester, Q2 is new semester)

1. activate Q1
2. run this script to download all assignments from Q1 in the time range
3. activate Q2
4. save each gradebook in QS - use `QSGradebookIterator`
5. run `upload_gradebook_data.py` to upload to Q2
6. reactivate Q1
7. run `delete_assignments.py` to delete the assignments posted to Q2
