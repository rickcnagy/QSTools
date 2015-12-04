"""
Add Grading Category ID

GETs the Grading Category IDs for a CSV of assignments from a defined section
with an assigment created for all required grading categories.

Requires: CSV of grading category names in a 'Category Name' column

Usage: ./add_grading_category_ids.py {schoolcode} {section_id} {filename}

Output: same CSV but with a 'Category ID' column
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    section_id = sys.argv[2]
    filename = sys.argv[3]
    q = qs.API(schoolcode)
    csv_grades = qs.CSV(filename)
    section_name = q.get_section(section_id)['sectionName']
    matched_categories = list()
    unmatched_categories = list()

    if section_name is None:
        raise ValueError("Section doesn't exist")
    if not ('Category Name') in csv_grades.cols:
        raise ValueError("'Category Name' column required")

    qs.logger.info("GETting grading categories based of the gradebook in section: " + section_name, cc_print=True)

    categories = q.get_grade_category_ids(section_id)

    for csv_grade in qs.bar(csv_grades):
        category_name = csv_grade['Category Name']
        if category_name in categories:
            csv_grade['Category ID'] = categories[category_name]
            matched_categories.append(category_name)
        else:
            unmatched_categories.append(category_name)

    # Return new csv if successful

    if 'Category ID' in csv_grade:
        qs.logger.info("Completed getting category ids. {} categories matched." .format(len(matched_categories)), cc_print=True)
        qs.logger.info("{} outstanding unmatched categories\n"  . format(len(unmatched_categories)), cc_print=True)
        filepath = qs.unique_path(csv_grades.filepath, suffix="w category IDs")
        csv_grades.save(filepath)
    else:
        qs.logger.info("Outstanding categories ({}) are unmatched\n" . format(len(unmatched_categories)), cc_print=True)
        for unmatched_category in unmatched_categories:
            qs.logger.info(unmatched_category, cc_print=True)


if __name__ == '__main__':
    main()
