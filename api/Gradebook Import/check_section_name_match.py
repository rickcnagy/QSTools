#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs

first_term = '18473'
second_term = '18714'

def main():
    good, bad = 0, 0
    bad_sections = []
    for section in qs.get_sections(semester_id=second_term):
        match = qs.match_section_by_info(section_name=section['sectionName'])
        if match:
            good += 1
        else:
            bad += 1
            bad_sections += section['sectionName']
    print good
    print bad

if __name__ == '__main__':
    main()
