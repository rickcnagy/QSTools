"""
Add Report Sessions ID's

GETs report cycle ids based on report cycle name entered into a csv. Currently,
sessions must have a unique name.

Requires: Database with Report Cycle naum, under a 'Report Cycle' column. The
'ignore_case' param is optional
Usage: ./add_report_cycles_ids.py {schoolcode} {filename}

Returns: the same csv, but with report cycle ids
"""


import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    csv_report_cycles = qs.CSV(filename)

    if 'Report Cycle' not in csv_report_cycles.cols:
        raise ValueError("'Report Cycle' column required")

    db_report_cycles = q.get_report_cycles()
    db_duplicates = qs.find_dups_in_dict_list(db_report_cycles, 'name')

    db_by_name = qs.dict_list_to_dict(db_report_cycles, 'name')

    if db_duplicates:
        qs.logger.info('Report Cycle names are not unique', cc_print=True)
    else:
        qs.logger.info('Report Cycle names are unique', cc_print=True)

    report_cycle_names_not_matched = set()
    for csv_report_cycle in csv_report_cycles:
        csv_report_cycle_name = csv_report_cycle['Report Cycle']

        if csv_report_cycle_name in db_duplicates:
            qs.logger.info('Report Cycle name has multiple matches', cc_print=True)

        db_match = db_by_name.get(csv_report_cycle_name)
        if db_match:
            csv_report_cycle['Report Cycle ID'] = db_match['id']
        else:
            report_cycle_names_not_matched.add(csv_report_cycle_name)

    if report_cycle_names_not_matched:
        qs.logger.warning(
            ('{} Report Cycles in the file were not found in the db'
                ''.format(len(report_cycle_names_not_matched))),
            report_cycle_names_not_matched)
    else:
        qs.logger.info('All Report Cycles were matched in the db.', cc_print=True)
        filepath = qs.unique_path(csv_report_cycles.filepath, suffix="with-report-cycle-IDs")
        csv_report_cycles.save(filepath)

if __name__ == '__main__':
    main()