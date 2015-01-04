#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Transform a file of criteria to dropdowns.

This takes a JSON file of of normal criteria, then outputs a JSON file with
dropdowns. The format is as in gui/importCriteria.js, so the output from here
can be used directly to import into the GUI.

The dropdodnws should be specified as they show up in the Setup Subject-
Specific Criteria page, such as:

    4,3,2,1,N/A

CLI Usage:
./transform_criteria_to_dropdowns.py {filename} [{dropdown_vals}]


dropdown_vals is optional, and will default to 4,3,2,1,N/A
"""

import sys
import json
import qs


def main():
    filename = sys.argv[1]
    dropdown_vals = sys.argv[2] if len(sys.argv) > 2 else '4,3,2,1,N/A'

    subject_templates = json.load(open(filename))

    for subject_template in subject_templates:
        original_criteria = subject_template['Criteria']
        new_criteria = []

        for criteria in original_criteria:
            if isinstance(criteria, dict):
                criteria = criteria.keys()[0]
            new_criteria.append({
                criteria: dropdown_vals
            })
        subject_template['Criteria'] = new_criteria

    qs.write_no_overwrite(qs.dumps(subject_templates), filename)

if __name__ == '__main__':
    main()
