#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools
import qs

filename = '/Users/Rick/Desktop/INTVLA Transcripts.csv'
csv = csv_tools.CSV(filename)


def main():
    teachers = {i['fullName']: i['id'] for i in qs.get_teachers()}
    csv.cols.append('New Section ID')
    for enrollment in csv:
        match = qs.matching_section_by_info(
            section_name=enrollment['Subject Name'].strip(),
            class_name=enrollment['Class Name'].strip(),
        )
        if not match:
            match = qs.matching_section_by_info(
                section_name=enrollment['Subject Name'].strip(),
            )
        if match:
            enrollment['New Section ID'] = match['id']
    csv.save()


if __name__ == '__main__':
    main()
