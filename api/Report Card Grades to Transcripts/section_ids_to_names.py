#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import json

cycle_3_semester_id = 15993
input_filename = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards sem 2.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards sem 2 filtered.json'

# for caching
qs.get_sections(semester_id=cycle_3_semester_id)

def main():
    new_data = {}
    old_data = json.load(open(input_filename))
    for student_id, section_data in old_data.iteritems():
        new_student_sections = {}
        for section_id, vals in section_data.iteritems():
            section_name = qs.get_section(section_id)['sectionName']
            filtered = filter_vals(vals)
            if filtered:
                new_student_sections[section_name] = filtered
                new_student_sections[section_name]['semester 2 id'] = section_id
        new_data[student_id] = new_student_sections
    json.dump(new_data, open(output_filename, 'w'), indent=4)

def filter_vals(vals):
    valid = ['s-marks-1', 's-marks-2', 's-letter-grade-1', 's-letter-grade-2']
    return {k: v for k, v in vals.iteritems() if k in valid and v and '-' not in v}

if __name__ == '__main__':
    main()
