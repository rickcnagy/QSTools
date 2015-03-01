#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Copy subject enrollment from all subjects on the backup server to live.

Run with Q1 active on live and backup

CLI usage:
./copy_enrollments_from_backup_server.py {schoolcode}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    backup = qs.API(schoolcode, 'backup')
    live = qs.API(schoolcode)

    for section_dict in qs.bar(backup.get_sections()):
        section_id = section_dict['id']
        backup_enrollment = backup.get_section_enrollment(section_id)
        backup_enrollment = backup_enrollment['students']
        enrolled_ids = [i['smsStudentStubId'] for i in backup_enrollment]

        if enrolled_ids:
            live.post_section_enrollment(section_id, enrolled_ids)

if __name__ == '__main__':
    main()
