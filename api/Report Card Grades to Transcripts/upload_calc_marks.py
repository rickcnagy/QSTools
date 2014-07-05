#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import api_logging
import qs
import json
from tqdm import tqdm

calc_marks_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA transcript upload data.json'
marks_upload_identifier = 'marks-calc'

def main():
    api_logging.config(__file__)
    calc_marks = json.load(open(calc_marks_filename))

    for student_id, section_dicts in tqdm(calc_marks.iteritems(), desc='POST', total=len(calc_marks)):
        upload_data = {}
        for section_name, section_dict in section_dicts.iteritems():
            section_id = section_dict['upload id']
            marks = section_dict['final average']
            upload_data[section_id] = {
                'values': {
                    marks_upload_identifier: marks
                }
            }
        qs.post_transcript_data(student_id, section_level=upload_data)


if __name__ == '__main__':
    main()
