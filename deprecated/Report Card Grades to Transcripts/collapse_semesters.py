#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json

sem1_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards sem 1 filtered.json'
sem2_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards sem 2 filtered.json'
output_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards combined.json'


def main():
    sem1 = json.load(open(sem1_file))
    sem2 = json.load(open(sem2_file))
    all_students = list(set(sem1.keys() + sem2.keys()))

    combined = {}
    for student_id in all_students:
        combined[student_id] = {}
        sem1_sections = {}
        sem2_sections = {}
        if student_id in sem1:
            sem1_sections = sem1[student_id]
        if student_id in sem2:
            sem2_sections = sem2[student_id]

        all_sections = list(set(sem1_sections.keys() + sem2_sections.keys()))
        for section_name in all_sections:
            sem1_vals = {}
            sem2_vals = {}
            if section_name in sem1_sections:
                sem1_vals = sem1_sections[section_name]
            if section_name in sem2_sections:
                sem2_vals = sem2_sections[section_name]
            combined[student_id][section_name] = dict(sem1_vals.items() + sem2_vals.items())
    json.dump(combined, open(output_file, 'w'), indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
