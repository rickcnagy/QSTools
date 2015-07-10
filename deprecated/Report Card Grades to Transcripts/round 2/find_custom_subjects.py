#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Find all 2013/2014 custom subjects that aren't on the RC but should be on
transcripts, per (1) on #32387
"""

import qs
import json
from tqdm import tqdm

output_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Custom Subjects.json'
twelfth_grade_id = '219063'


def main():
    qs.api_logging.config(__file__)
    twelfth_grader_ids = [
        i['id'] for i in qs.get_students()
        if 'classId' in i and i['classId'] == twelfth_grade_id
    ]

    to_be_moved = {}
    for student_id in tqdm(twelfth_grader_ids, desc='GET'):
        data = qs.get_transcript_data(student_id)

        custom_semester_id = current_custom_semester_id(data)
        if not custom_semester_id: continue

        current_custom_subjects = {
            k: v for k, v in data['sectionLevel'].iteritems()
            if 'semester-id' in v
                and v['semester-id'] == custom_semester_id
        }

        valid_semester_ids = [i['id'] for i in qs.get_semesters_from_year()]
        current_actual_subject_names = [
            v['subject-name'] for k, v in data['sectionLevel'].iteritems()
            if 'C' not in k
                and qs.get_section(k)['smsAcademicSemesterId'] in valid_semester_ids
        ]

        to_be_moved[student_id] = {
            k: v for k, v in current_custom_subjects.iteritems()
            if 'subject-name' in v
                and v['subject-name'].strip() not in current_actual_subject_names
        }
        to_be_moved[student_id].update({'actual subjects': current_actual_subject_names})
    json.dump(to_be_moved, open(output_filename, 'w'), indent=4)


def current_custom_semester_id(data):
    for semester_id, semester_answers in data['semesterLevel'].iteritems():
        if ('C' in semester_id
                and 'year-name' in semester_answers
                and '2014' in semester_answers['year-name']):
            return semester_id[2:]

if __name__ == '__main__':
    main()
