#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools

year = '2013/2014'
csv_file = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Gradebook Data - Final.csv'
output_file = ('/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Enrollment {}.csv'
    .format(year.replace('/', '-')))
csv = csv_tools.CSV(csv_file)


def main():
    # {student: {class: 11, courses:[course1, course2]}}
    output = {}
    csv.rows = [row for row in csv if row['School Year'] == year]
    for row in csv:
        name = row['Student Name']
        if name not in output.keys():
            output[name] = {
                'class': row['Grade Level'],
                'courses': []
            }
        output[name]['courses'].append(row['Course Name'])

    output_list = []
    for student_name, row in output.iteritems():
        class_code = row['class']
        if int(class_code) < 10:
            class_code = '0' + class_code
        class_code = 'G' + class_code

        output_list.append({
            'Student Name': student_name,
            'Class Abbreviation': class_code,
            'Courses': row['courses'],
        })
    csv_tools.list_to_csv(output_list, output_file)


if __name__ == '__main__':
    main()
