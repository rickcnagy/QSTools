Utility Scripts
===

####[`csv2json.py`](./csv2json.py)

Module for converting CSV's to JSONArray's of Row objects.
Usage is as follows:
./csv2json.py {filepath1} {filepath2} {...}


####[`fill_in_pivot.py`](./fill_in_pivot.py)

Fill in a pivot table CSV such that this:
+------+------+------+
| Col1 | Col2 | Col3 |
+------+------+------+
|    1 |    1 |    1 |
|      |      |    2 |
|      |    2 |    4 |
|      |      |    5 |
+------+------+------+

Turns into this:
| Col1 | Col2 | Col3 |
+------+------+------+
|    1 |    1 |    1 |
|    1 |    1 |    2 |
|    1 |    2 |    4 |
|    1 |    2 |    5 |
+------+------+------+

Example input sheet:
examples/fill_in_pivot.sample.csv

CLI Usage:
python fill_in_pivot.py {pivot CSV filename}


####[`folder_pdf_page_count.py`](./folder_pdf_page_count.py)

Utility script to analyze page count in report cards in the current dir.

This counts the number of pages in each RC and compares to the target length.
For schools where the number of pages is important, this is a great way to
get an overview of what changes need to be made.

Searches the current directory (non recursively) for PDF's and counts their
pages.

CLI Usage:
folder_pdf_page_count.py {schoolcode} {target_length}

The target length is how long we *want* the PDF's to be.


####[`parse_criteria_txt_file.py`](./parse_criteria_txt_file.py)

Parse a subject criteria template file.

This creates a JSON file that can be directly used in gui/importCriteria.js

args:
    1: Pass in the filename to open

CLI Usage:
./parse_criteria_txt_file.py {filename}

The txt file should be formatted like so:

    Subject Template Name1
    Criteria 1.1
    Criteria 1.2
    Criteria 1.3

    Subject Template Name3
    Criteria 2.1
    Criteria 2.2
    Criteria 2.3

To import dropdowns, run the export from this through
./transform_criteria_to_dropdowns.py

Alternative subject section names aren't currently supported


####[`readme_generator.py`](./readme_generator.py)

Generate README from in files in folder passed in via stdin

Command Line Args (in order):
    path to README directory
    (optional) README title
Example Usage:
./utility/readme_generator.py ./api 'API Scripts'


####[`titlecase_all.py`](./titlecase_all.py)

Titlecase all cells (except for headers) in a CSV

CLI Usage:
python titlecase_all.py filepath


####[`transform_criteria_to_dropdowns.py`](./transform_criteria_to_dropdowns.py)

Transform a file of criteria to dropdowns.

This takes a JSON file of of normal criteria, then outputs a JSON file with
dropdowns. The format is as in gui/importCriteria.js, so the output from here
can be used directly to import into the GUI.

The dropdodnws should be specified as they show up in the Setup Subject-
Specific Criteria page, such as:

    4,3,2,1,N/A

CLI Usage:
./transform_criteria_to_dropdowns.py {filename} [{dropdown_vals}]


dropdown_vals is optional, and will default to 4,3,2,1,N/A


####[`zeus_xml/`](./zeus_xml)
