"""
Add Class ID

GETs the class ID for a particular class by class name.

Requires: CSV with column of class names, 'Class Name' or 'Grade'

Usage: ./add_class_ids.py {schoolcode} {filename.csv} {ignore_case}

Output: same CSV but with a column of class id's
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    ignore_case = bool(sys.argv[3]) if len(sys.argv) > 3 else True
    csv_classes = qs.CSV(filename)
    q = qs.API(schoolcode)

    if not ('Class Name' in csv_classes.cols or ('Grade' in csv_classes.cols) or ('Grade Level' in csv_classes.cols)):
        raise ValueError('Class Name, Grade Level, or Grade column required.')

    db_classes = q.get_classes()
    db_duplicates = qs.find_dups_in_dict_list(db_classes, 'name')

    if db_duplicates:
        qs.logger.critical(
            'Class Names are not unique in DB, duplicates:',
            db_duplicates)
    else:
        qs.logger.info('class names are unique.')

    if ignore_case is True:
        for class_name in db_classes:
            class_name['name'] = class_name['name'].lower()
    db_by_name = qs.dict_list_to_dict(db_classes, 'name')

    class_names_not_matched = set()
    for csv_class in csv_classes:
        if 'Class Name' in csv_class:
            csv_class_name = csv_class['Class Name']
        elif 'Grade' in csv_class:
            csv_class_name = csv_class['Grade']
        else:
            csv_class_name = csv_class['Grade Level']

        csv_orginal_class_name = csv_class_name
        if ignore_case:
            csv_class_name = csv_class_name.lower()
        db_match = db_by_name.get(csv_class_name)
        if db_match:
            csv_class['Class ID'] = db_match['id']
        else:
            class_names_not_matched.add(csv_orginal_class_name)

    if class_names_not_matched:
        qs.logger.warning(
            ('{} classes in the file were not found in the db'
                ''.format(len(class_names_not_matched))),
            class_names_not_matched)
    else:
        qs.logger.info('All classes were matched in the db.', cc_print=True)
        filepath = qs.unique_path(csv_classes.filepath, suffix="with student IDs")
        csv_classes.save(filepath)

if __name__ == ('__main__'):
    main()
