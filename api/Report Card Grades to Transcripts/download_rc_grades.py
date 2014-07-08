#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import data_migration
import qs

REPORT_CYCLE_ID = '5865'


def main():
    data_migration.create_file('report card data download')
    qs.api_logging.config(__file__, log_filename=data_migration.get_filename())
    data_migration.check_before_run()

    # { studentID: {sectionId1: {marks: 100, grade: A}, sectionID2:{..}}, studentId2: {..}}
    all_rc_data = {}
    student_ids = [i['id'] for i in qs.get_students()]
    for student_id in data_migration.indicator(student_ids, 'GET'):
        report_card = qs.get_report_card_data(student_id, REPORT_CYCLE_ID)
        all_rc_data[student_id] = report_card['sectionLevel']
    data_migration.save(all_rc_data)


if __name__ == '__main__':
    main()
