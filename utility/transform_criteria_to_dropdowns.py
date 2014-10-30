#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import qs

FILENAME = ''
TARGET_DROPDOWN = '4,3,2,1,N/E'


def main():
    subject_templates = [
        i for i in json.load(open(FILENAME))
        if 'Preschool' not in i['Template Name']
    ]

    for subject_template in subject_templates:
        original_criteria = subject_template['Criteria']
        new_criteria = []

        for criteria in original_criteria:
            if isinstance(criteria, dict):
                criteria = criteria.keys()[0]
            new_criteria.append({
                criteria: TARGET_DROPDOWN
            })
        subject_template['Criteria'] = new_criteria
    json.dump(subject_templates, open(qs.unique_path(FILENAME), 'w'))

if __name__ == '__main__':
    main()
