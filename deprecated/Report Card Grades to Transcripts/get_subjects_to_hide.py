#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import api_logger
import qs
import json
import csv_tools

calc_marks_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA transcript upload data.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA subjects to hide.csv'

def main():
    calc_marks = json.load(open(calc_marks_filename))
    rows = []
    cols = ['Student Name', 'Student ID', 'Subjects to Hide']
    for student_id, sections in tqdm(calc_marks.iteritems(), total=len(calc_marks)):
        transcript_sections = qs.get_transcript_data(student_id)
        transcript_section_names = [
            qs.get_section(i)['sectionName'] for i
            in transcript_sections
        ]
        to_remove = [i for i in transcript_section_names if i not in sections.keys()]
        rows.append({
            cols[0] = qs.get_student(student_id)['fullName'],
            cols[1] = student_id,
            cols[2] = to_remove
        })
    csv_tools.write_csv(rows, output_filename, keys=cols)


if __name__ == '__main__':
    main()
