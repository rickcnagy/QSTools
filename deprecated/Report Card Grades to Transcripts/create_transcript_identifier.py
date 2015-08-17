#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
from tqdm import tqdm


def main():
    student_ids = [i['id'] for i in qs.get_students()]
    for student_id in tqdm(student_ids):
        qs.get_transcript_data(student_id)


if __name__ == '__main__':
    main()
