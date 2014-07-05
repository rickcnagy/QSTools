#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import qs
import api_logging

custom_subject_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Custom Subjects - hand checked.json'


def main():
    api_logging.config(__file__)
    custom_subjects = json.load(open(custom_subject_filename))
    for student_id, subjects in custom_subjects.iteritems():
        online_custom_ids = get_custom_subject_ids(student_id)
        offline_subject_dicts = [{
                k: v for k, v in d.iteritems()
                if k in ['subject-name', 'letter-grade', 'credit-earned']
            } for _, d in subjects.iteritems()
        ]
        merged = {
            online_custom_ids[i]: subject_dict
            for i, subject_dict in enumerate(offline_subject_dicts)
        }
        upload_merged(student_id, merged)
        break


def get_custom_subject_ids(student_id):
    transcript_data = qs.get_transcript(student_id)
    current_semester_id = next(
        v['semester-id']
        for k, v in transcript_data['semesterLevel'].iteritems()
        if v['year-name'] == '2013/2014'
    )
    return [
        k for k, v in transcript_data['sectionLevel'].iteritems()
        if 'C' in k
            and v['subject-name'] == ' '
            and v['semester-id'] == current_semester_id
    ]


def upload_merged(student_id, merged):
    to_upload = {k: {'values': v} for k, v in merged.iteritems()}
    qs.post_transcript(student_id, section_level=to_upload)


if __name__ == '__main__':
    main()
