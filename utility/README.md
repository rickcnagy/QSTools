Utility Scripts
===

####[`csv2json.py`](./csv2json.py)

Module for converting CSV's to JSONArray's of Row objects.
Usage is as follows:
./csv2json.py {filepath1} {filepath2} {...}


####[`folder_pdf_page_count.py`](./folder_pdf_page_count.py)

Utility script to analyze page count in report cards.

This counts the number of pages in each RC and compares to the target length.
For schools where the number of pages is important, this is a great way to
get an overview of what changes need to be made.

Searches the current directory (non recursively) for PDF's and counts their
pages.

CLI Usage:
folder_pdf_page_count.py {schoolcode}

If schoolcode is supplied (optional), then each student's class will be printed
along with their name


####[`readme_generator.py`](./readme_generator.py)

Generate README from in files in folder passed in via stdin

Command Line Args (in order):
    path to README directory
    (optional) README title
Example Usage:
./utility/readme_generator.py ./api 'API Scripts'


####[`zeus_xml/`](./zeus_xml)
