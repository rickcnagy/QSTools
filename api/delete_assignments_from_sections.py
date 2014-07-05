#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Delete assignments with specified ids from the specified sections.
Put in all of the sections known and assignments known and the script will match them.
This has the advantage that the specific assignment-section mapping doesn't have to be known.
"""

import qs
import api_logging
import json
import data_migration

assignments_to_delete = ["1070075", "1070076", "1070077", "1070078", "1070079", "1070080", "1070081", "1070082", "1070083", "1070084", "1070085", "1070086", "1070087", "1070088", "1070089", "1070090", "1070091", "1070092", "1070093", "1070094", "1070095", "1070096", "1070097", "1070098", "1070099", ]
sections = ['635771']

def main():
    api_logging.config(__file__)

    # {section: [assignments]}
    to_delete = {qs.match_section_by_id(i)['id']: [] for i in sections}
    for section_id, assignments in to_delete.iteritems():
        assignments += [
            i['id']
            for i in qs.get_assignments(section_id)
            if i['id'] in assignments_to_delete
        ]

    print "will delete:"
    print json.dumps(to_delete, indent=4)
    if data_migration.confirm():
        for section, assignments in to_delete.iteritems():
            for assignment in assignments:
                qs.delete_assignment(section, assignment)


if __name__ == '__main__':
    main()
