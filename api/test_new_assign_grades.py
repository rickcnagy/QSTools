""" test posting assignments and things """
import qs
import sys

def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    q = qs.API(schoolcode)

    section = 634488
    name = 'assign'
    date = 2015-05-15
    marks = 90.6
    category = 38950
    grading_scale = 15065

    new_assignment = q.post_assignment(section, name, date, marks, category, grading_scale

    assignment = new_assignment['id']

    new_grade = q.post_grade(section, assignment, marks)

    qs.pp({"section": section, "new assignment id": new_assignment['id'], "new grade id":new_grade['id']})

if __name__ == '__main__':
    main()
