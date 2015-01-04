#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Parse a subject criteria template file.

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
"""

import sys
import qs
import json


def main():
    filename = sys.argv[1]

    subject_blocks = open(filename, 'rU').read().split('\n\n')
    subject_blocks = [i.split('\n') for i in subject_blocks]

    subject_templates = []
    for subject_block in subject_blocks:
        subject_template = {}
        subject_templates.append(subject_template)

        subject_template['Template Name'] = subject_block.pop(0)
        subject_template['Alternative Subject Section Name'] = ''
        subject_template['Criteria'] = [i.strip() for i in subject_block]

    output = qs.dumps(subject_templates)
    qs.write_no_overwrite(output, filename, extension='json')

if __name__ == '__main__':
    main()
