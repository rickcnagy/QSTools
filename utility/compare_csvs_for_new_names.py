"""
Compare CSV for New Names

This script looks at 2 csv's of name data to find unique names. The unique
names are returned on a new spreadsheet, with all of their data, and the
duplicates are excluded (though a list of these is printed out). The second csv
is compared against the first, i.e. the "base" is filename1.csv and the
comparison is filename2.csv. The names that do not appear in filename1.csv
but are in filename2.csv will be the ones returned. Assumes no duplicate names.

Requires: 2 csv's, each with a Full Name column

Usage: ./compare_csvs_for_new_names.py {filename1.csv} {filename2.csv}

Returns: spreadsheet of names who appear in filename2.csv, but not in
filename1.csv
"""

import qs
import sys


def main():
    qs.logger.config(__file__)
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    csv_orig_names = qs.CSV(filename1)
    csv_new_names = qs.CSV(filename2)

    orig_names = []
    new_names = []
    unique_names = []
    duplicate_names = []
    new_csv_data = []

    if 'Full Name' not in csv_orig_names.cols:
        raise ValueError("'Full Name' column required in original names csv")
    if 'Full Name' not in csv_new_names.cols:
        raise ValueError("'Full Name' column required in new names csv")
    
    # Make lists of duplicate and unique names

    for name in csv_orig_names:
        name_name = name['Full Name']
        orig_names.append(name_name)

    for name in csv_new_names:
        name_name = name['Full Name']
        new_names.append(name_name)

    for name in new_names:
        qs.logger.info(name, cc_print=False)
        if name in orig_names:
            duplicate_names.append(name)
        else:
            unique_names.append(name)

    # Write CSV of unique names

    for name in csv_new_names:
        name_name = name['Full Name']
        if name_name in unique_names:
            new_csv_data.append(name)

    qs.logger.info('Duplicate names ({}) (not returned in output csv):' .format(len(duplicate_names)),
                   cc_print=True)
    qs.logger.info(qs.dumps(duplicate_names), cc_print=True)
    qs.logger.info('Unique names ({}) (returned):' .format(len(unique_names)), cc_print=True)
    qs.logger.info(qs.dumps(unique_names), cc_print=True)

    if unique_names:
        qs.write_csv(new_csv_data, '~/Desktop/unique_names.csv')
    else:
        qs.logger.info("No file generated.", cc_print=True)

if __name__ == ('__main__'):
    main()