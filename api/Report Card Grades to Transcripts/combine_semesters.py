#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import qs

cycle_3_semester_id = '15993'
sem1_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards sem 1.json'
sem2_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards sem 2.json'

def main():
    qs.api_logging.config(__file__)
    sem1 = json.load(open(sem1_file))
    sem2 = json.load(open(sem2_file))

    all_student_ids = list(set(sem1.keys() + sem2.keys()))

    # for cache
    qs.get_sections(semester_id=cycle_3_semester_id)

    for student_id in all_student_ids:
        sem1_section_ids = sem1[student_id]
        sem2_section_ids = sem2[student_id].keys()

        sem1_sections = [qs.get_section(i) for i in sem1_section_ids]
        sem2_matched = [qs.match_section_by_name(i['sectionName']) for i in sem1_sections]
        sem2_matched_ids = [i['id'] for i in sem2_matched if i]

        print sem2_section_ids
        print sem2_matched_ids
        print
        print


if __name__ == '__main__':
    main()
