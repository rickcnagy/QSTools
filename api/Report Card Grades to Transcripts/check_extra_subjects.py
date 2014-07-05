#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""Right now, this just checks the number of subjects in each semester, which isn't too helpful.
What's actually necessary is to lookup all the subjects (by name) that aren't specified in the upload file
This will be done after the upload is complete."""


import json
import qs
import tqdm
import api_logging

filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA transcript upload data.json'
end_of_year_session = ''

def main():
    api_logging.config(__file__)
    to_upload = json.load(open(filename))
    for student_id in to_upload:
        print qs.get_student(student_id)['fullName']

        report_cycles = [
            i
            for i in qs.get_report_cycles()
            if 'Report Card' in i['name'] and '2013-2014' in i['name']
        ]
        for report_cycle in report_cycles:
            end_of_year_subjects = qs.get_report_card_data(student_id, report_cycle_id)['sectionLevel']
            print report_cycle['name']
            report_cycle_id = report_cycle['id']
            subject_len = len(qs.get_report_card_data(student_id, report_cycle_id)['sectionLevel'])
            print subject_len
        print
        print


if __name__ == '__main__':
    main()
