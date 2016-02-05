#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""
Tools for taking care of boiler-plate things in the average python script for
manipulating data for use with the API
"""


def check_for_csv_columns(self, columns, required_columns,
        alternate_columns=None):
    """
    Checks for required columns in list of columns from an opened csv. Takes
     the following paramenter:
     columns - List of columns in the csv. Usually, somthing like csv.cols
        makes sense, if using csv_tools from this module
    required_columns - List of columns needed in the csv for the script
    alternate_columns - Dict of alternate column options. For
        example:
            {'Student Name': ['Full Name', ['First', 'Last']]}
            {'Teacher Name': ['Teacher']}
    """
    for column in columns:
        missing_columns = []
        if column not in required_columns:
            missing_columns.add(column)

    if (missing_columns and alternate_columns):
        for column in missing_columns:
            if column in alternate_columns:
                missing_columns.delete(column)
            else:
                missing_columns.delete(column)
                missing_columns.append(column + missing_columns[column])

    if missing_columns:
        qs.logger.info("Missing Columns Found", cc_print=True)
        for column in missing_columns:
            qs.logger.info(column, cc_print=True)
        qs.logger.critical("Please update file with the " + len(missing_columns) + " found.", cc_print=True)



