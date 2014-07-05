#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import api_logging
import qs
import json
from tqdm import tqdm
import csv_tools

calc_marks_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA transcript upload data.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA subjects to hide.csv'
cols = ['Student Name', 'Student ID', 'Subjects to Hide']
rows = []
current_year_id = '11627'


def main():
    api_logging.config(__file__)
    calc_marks = json.load(open(calc_marks_filename))

    for student_id, sections in tqdm(calc_marks.iteritems(), total=len(calc_marks), desc='GET'):
        transcript_data = qs.get_transcript_data(student_id)['sectionLevel']
        manage_subjects_to_hide(transcript_data, sections, student_id)

        to_post = {}
        for section_id, data in transcript_data.iteritems():
            if data['marks-calc']:
                to_post[section_id] = {
                     'values': {
                        'letter-grade': data['letter-grade-calc']
                    }
                }
        qs.post_transcript_data(student_id, section_level=to_post)
    csv_tools.write_csv(rows, output_filename, keys=cols)


def manage_subjects_to_hide(transcript_sections, offline_sections, student_id):
    global rows
    valid_semesters = [i['id'] for i in qs.get_semesters_from_year()]
    transcript_sections = [
        i for i in transcript_sections
        if 'C' not in i
            and qs.get_section(i)['smsAcademicSemesterId'] in valid_semesters
    ]
    transcript_section_names = [
        qs.get_section(i)['sectionName']
        for i in transcript_sections
    ]
    to_remove = [
        i for i in transcript_section_names
        if i not in offline_sections.keys()
    ]
    rows.append({
        cols[0]: qs.get_student(student_id)['fullName'],
        cols[1]: student_id,
        cols[2]: to_remove
    })

if __name__ == '__main__':
    main()
