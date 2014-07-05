#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools
import qs
import api_logging
from tqdm import *

SEMESTER_IDS = ['20267', '20270', '20273', '20276', '20266', '20269', '20272', '20275', '20265', '20268', '20271', '20274', '20261', '20262', '20263', '20264', '18473', '18714']
csv = csv_tools.CSV('/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Gradebook Data - Final.csv')


def main():
    api_logging.basicConfig(__file__)
    for semester_id in tqdm(SEMESTER_IDS):
        semester = [i for i in qs.get_semesters() if i['id'] == semester_id][0]
        quarter = quarter_from_name(semester['semesterName'])
        year = semester['yearName']
    
        # {section_id: [student_id1, student_id2]}
        csv_enrollment = {}
        for row in [i for i in csv if i['School Year'] == year]:
            section_id = row['Q{} SectionID'.format(quarter)]
            if not section_id in csv_enrollment:
                csv_enrollment[section_id] = []
            csv_enrollment[section_id].append(row['Student ID'])

        # [{Course Name: blah, 'To Enroll': [], 'To Unenroll': []}]
        diffs = []
        sections_by_id = {i['id']: i for i in qs.get_sections(semester_id=semester_id)}
        for section_id, enrollment in csv_enrollment.iteritems():
            online_enrollment = [
                i['smsStudentStubId']
                for i
                in qs.get_section_enrollment(section_id)]
            missing_from_online = [i for i in enrollment if i not in online_enrollment]
            missing_from_csv = [i for i in online_enrollment if i not in enrollment]
            if missing_from_csv or missing_from_online:
                section = sections_by_id[section_id]
                diffs.append({
                    'Course Name': section['sectionName'],
                    'Course Code': section['sectionCode'],
                    'Course Grade Level': section['className'],
                    'Course Teacher(s)': [i['fullName'] for i in section['teachers']],
                    'Course ID': section_id,
                    'Students to Enroll': qs.student_ids_to_names(missing_from_online),
                    'Students to Unenroll': qs.student_ids_to_names(missing_from_csv),
                })
        output = output_filename(year, quarter)
        csv_tools.rows_to_csv(diffs, output, keys=[
            'Course Name',
            'Course Code',
            'Course Grade Level',
            'Course Teacher(s)',
            'Course ID',
            'Students to Enroll',
            'Students to Unenroll',
        ])
        print "Finished semester: " + output


def output_filename(year, quarter):
    return ('/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Enrollment - Quarter {} {}.csv'.format(
        quarter, year.replace('/', '-')))

def quarter_from_name(quarter_name):
    return {'First Term': 1, 'Second Term': 2, 'Third Term': 3, 'Fourth Term': 4}[quarter_name]

if __name__ == '__main__':
    main()
