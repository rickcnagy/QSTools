#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Find all 2013/2014 custom subjects that aren't on the RC but should be on
transcripts, per (1) on #32387
"""

import qs

def main():
    qs.api_logging.config(__file__)
    for student_id in [i['id'] for i in qs.get_students()]:
        print student_id
        data = qs.get_transcript_data(student_id)
        custom_semester_id = current_custom_semester_id(data)


def current_custom_semester_id(data):
    found = 0
    for semester_id, semester_answers in data['semesterLevel'].iteritems():
        if ('C' in semester_id
                and 'year-name' in semester_answers
                and '2014' in semester_answers['year-name']):
            found += 1
    print found if found < 2 else "PROBLEM"
    print

if __name__ == '__main__':
    main()
