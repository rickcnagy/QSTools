#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools

sem1_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report card data download_sa_53 sem 1.csv'
sem2_file = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report card data download_sa_12 sem 2.csv'

def main():
    sem1 = csv_tools.CSV(sem1_file)
    sem2 = csv_tools.CSV(sem2_file)
    all_rows = sem1.rows + sem2.rows

    sem1_students = [i['student_id'] for i in sem1]
    sem2_students = [i['student_id'] for i in sem2]
    all_students = list(set(sem1_students + sem2_students))

    all_student_data = {}
    for student in all_students:
        student_rows = [i for i in all_rows if i['student_id'] == student]
        student_sections = [i['section_id'] for i in student_rows]
        for section in student_sections:
            section_rows = [i for i in student_rows if i['section_id'] == section]
            print len(section_rows)


if __name__ == '__main__':
    main()
