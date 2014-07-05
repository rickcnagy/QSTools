#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools
import json

input_filename = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report card data download_sa_53.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report card data download_sa_53 sem 1.csv'


def main():
    data = json.load(open(input_filename))
    rows = []
    cols = ['student_id', 'section_id', 's-marks-1', 's-marks-2', 's-letter-grade-1', 's-letter-grade-2']
    for student_id, section_ids in data.iteritems():
        for section_id, section_level_identifiers in section_ids.iteritems():
            row = {}
            row['student_id'] = student_id
            row['section_id'] = section_id
            row.update({
                i: val
                for i, val in section_level_identifiers.iteritems()
                if i in cols
            })
            print row
            rows.append(row)

    csv_tools.write_rows_to_csv(rows, output_filename, keys=cols)

if __name__ == '__main__':
    main()
