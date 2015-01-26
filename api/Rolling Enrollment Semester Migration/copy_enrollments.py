#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Run with Q1 active on live and backup"""

import qs


def main():
    qs.logger.config(__file__)
    backup = qs.API('intvla2', 'backup')
    live = qs.API('intvla2', 'local')

    for section_id in qs.bar(backup.get_sections()):
        backup_enrollment = backup.get_section_enrollment(section_id)
        enrolled_ids = [i['smsStudentStubId'] for i in backup_enrollment]

        live.post_section_enrollments(enrolled_ids)

if __name__ == '__main__':
    main()
