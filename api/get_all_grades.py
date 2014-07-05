#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs


def main():
    sections = qs.get_all_sections()
    
    for section in sections:
        print("\n{}, {}".format(
            section['sectionName'], section['teachers'][0]['fullName']
        ))
        
        assignments = qs.get_assignments(section['id'])
        if not assignments:
            continue

        for assignment in assignments:
            print assignment['date']


if __name__ == '__main__':
    main()
