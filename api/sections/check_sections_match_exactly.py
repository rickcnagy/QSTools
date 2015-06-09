#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Check that all sections in source_semester have an exact match in the active semester"""



import qs

source_semester = '17900'

def main():
    qs.api_logging.config(__file__)

    source_sections = qs.get_sections(semester_id=source_semester)
    bad = good = 0
    mismatches = []
    for section in source_sections:
        match = qs.match_section_by_dict(section)
        if not match:
            bad += 1
            mismatches.append(section['id'])
        else:
            qs.api_logging.info('Match: {} in {} --> {}'.format(
                section['id'], source_semester, match['id']), {
                    'source': section,
                    'match': match,
                }, cc_print=False)
            good += 1
    print 'bad: {}\ngood: {}'.format(bad, good)
    print mismatches


if __name__ == '__main__':
    main()
