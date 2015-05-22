#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
'''
delete assignments after they've been migrated via upload_gradebook_data.py
'''

from tqdm import *
import qs
import data_migration


def main():
    data_migration.create_file(prefix="delete", existing_file=True)
    qs.api_logging.basicConfig(__file__, log_filename=data_migration.get_filename())
    data_migration.check()
    valid_assignments = data_migration.load("download")
    posted_assignment_ids = data_migration.load("upload")

    if raw_input("delete {} assignments? (y):\n".format(len(posted_assignment_ids))) != 'y':
        qs.api_logging.critical("user aborted")

    for i in trange(0, len(valid_assignments), desc='DEL', leave=True):
        section_id = valid_assignments.keys()[i]

        for assignment in valid_assignments[section_id]:
            assignment_id = assignment['assignmentId']
            if not assignment_id in posted_assignment_ids: continue

            qs.delete_assignment(section_id, assignment['assignmentId'])
    data_migration.complete()


if __name__ == '__main__':
    main()
