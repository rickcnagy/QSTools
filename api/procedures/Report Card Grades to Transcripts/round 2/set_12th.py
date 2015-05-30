#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import qs
from tqdm import *

data_file = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Custom Subjects - hand checked.json'


def main():
    qs.api_logging.config(__file__)
    data = json.load(open(data_file))
    for student_id in tqdm(data, desc='GET'):
        transcript = qs.get_transcript(student_id)
        semester_id = next(
            k for k, v in transcript['semesterLevel'].iteritems()
            if v['year-name'] == '2013/2014'
        )
        qs.post_transcript(student_id, semester_level={
            semester_id: {
                'values': {
                    'class-level': qs.get_student(student_id)['className']
                }
            }
        })


if __name__ == '__main__':
    main()
