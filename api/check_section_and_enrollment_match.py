#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Check that SOURCE_SEMESTER matches the current semester in both enrollment and sections."""


import qs
import json

SOURCE_SEMESTER = 17900

def main():
    discrepencies = qs.enrollment_discrepancies(SOURCE_SEMESTER)
    if discrepencies:
        print "There are discrepencies:\n" + json.dumps(discrepencies)
    else:
        print "There are no discrepencies in sections or enrollments!"


if __name__ == '__main__':
    main()
