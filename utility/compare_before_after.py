"""
Compare Data Before & After

Use this script to compare the values of a pair of fields in two different
columns on the same row of data. Great for things like when it's not clear that
GETtting the sections ids are going to be the same (depending if they are
retrieved based on enrollment and semester name). Optional param to disregard a
value that appears in either column as a not-real...i.e. treat it like it's
if that value shows up in a cell, then it's actually empty.

Assumptions:
Either Student ID or Teacher ID columns exist
Full Name column exists

Requirements
Two column headers, passed in as key_1 and key_2


Usage:

./compare_before_after {key_1} {key_2} {filename} {disregard_value}

Returns:
CSV with columns for Full Name, ID (student/teacher), two fields compared
and a new column for "Comparison". If the two keys match OR one key is compared
to a blank value (including the 'disregard_value), "TRUE" is returned
otherwise "FALSE" is returned in a new 'Comparison' column

"""


import sys
import qs


def main():
    qs.logger.config(__file__)
    qs.logger.info('Setting up and opening file...',cc_print=True)

    key_1 = sys.argv[1]
    key_2 = sys.argv[2]
    filename = sys.argv[3]
    if len(sys.argv) > 4:
        disregard_value = sys.argv[4]
    csv_data_file = qs.CSV(filename)

    compared_rows = []
    headers = []
    successful_comparisons = 0
    unsuccessful_comparisons = 0

    # Check for required columns

    if not ('Student ID' or 'Teacher ID') in csv_data_file.cols:
        missing_columns = ['Student ID or Teacher ID']
        if ('Teacher ID' in csv_data_file.cols) and ('Teacher Name'):
            missing_columns.append('Teacher Name')
        else:
            missing_columns.append('Full Name or First & Last')

        if missing_columns:
            for missing_column in missing_columns:
                print "Column Missing: {}" . format(missing_column)
            sys.tracebacklimit = 0
            raise ValueError("Columns are missing from CSV. See above for details.")

    # Make headers for output file

    if 'Student ID' in csv_data_file.cols:
        headers.append('Student ID')
    else:
        headers.append('Teacher ID')

    if 'Full Name' in csv_data_file.cols:
        headers.append('Full Name')
    elif 'Teacher Name' in csv_data_file.cols:
        headers.append('Teacher Name')
    else:
        headers.append('First')
        headers.append('Last')

    headers.append(key_1)
    headers.append(key_2)
    headers.append('Comparison')

    # Actually compare things

    qs.logger.info('Comparing values...', cc_print=True)
    for row in qs.bar(csv_data_file):
        if 'Student ID' in csv_data_file.cols:
            person_id = row['Student ID']
            id_type = 'Student ID'
            if 'Full Name' in csv_data_file.cols:
                name = row['Full Name']
                name_type = 'Full Name'
            else:
                first = row['First']
                last = row['Last']
        else:
            person_id = row['Teacher ID']
            name_type = 'Teacher ID'
            name = row['Teacher Name']
            name_type = 'Teacher Name'

        key_1_value = row[key_1]
        key_2_value = row[key_2]

        comparison = ''
        if key_1_value == disregard_value:
            comparison = 'TRUE'
            successful_comparisons += 1
        elif key_2_value == disregard_value:
            comparison = 'TRUE'
            successful_comparisons += 1
        else:
            if key_1_value == key_2_value:
                comparison == 'TRUE'
                successful_comparisons += 1
            else:
                comparison == 'FALSE'
                unsuccessful_comparisons += 1

        if ('First' and 'Last') in csv_data_file.cols:
            new_row = {id_type: person_id, 'First': first, 'Last': last,
                key_1: key_1_value, key_2: key_2_value, 'Comparison': comparison}
        else:
            new_row = {id_type: person_id, name_type: name,
                key_1: key_1_value, key_2: key_2_value, 'Comparison': comparison}
        
        qs.logger.info(new_row)
        
        compared_rows.append(new_row)

    qs.logger.info('Comparison Complete', cc_print=True)
    qs.logger.info('Successful Comparisons: ', successful_comparisons, cc_print=True)
    qs.logger.info('Unsuccessful Comparisons: ', unsuccessful_comparisons, cc_print=True)

    new_filepath = filepath.rstrip('.csv') + ('_processed.csv')
    qs.write_csv(compared_rows, new_filepath, column_headers=headers)


if __name__ == '__main__':
    main()
