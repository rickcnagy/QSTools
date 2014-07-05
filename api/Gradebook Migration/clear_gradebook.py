#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
from tqdm import *

def main():
    section_ids = ['674657', '675224', '674719']
    for section_id in section_ids:
        assignments = qs.get_assignments(section_id)
        for assignment in assignments:
            qs.delete_assignment(section_id, assignment['id'])

if __name__ == '__main__':
    main()