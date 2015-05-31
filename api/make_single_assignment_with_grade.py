"""
    Make Single Assignment with grade

    Similar to upcoming wrapper function, this script makes an assignment
    and posts a grade to it for a single student. Just in case you want to
    do this via API for some reason.

    Usage:
    ./make-single-assignment-with-grade-py schoolcode studentID
        name_of_assignment date total_possible_points
        category_id marks grading_scale_id section_id

    Please note, the name must be in a 'string' format and the
    date must be in a YYYY-MM-DD format

    Requires: valid ids

    Returns: success message, and if successful, will post a grade
"""
import qs
import sys


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    q = qs.API(schoolcode)
    student = sys.argv[2]
    assign_name = sys.argv[3]
    assign_date = sys.argv[4]
    total_possible = sys.argv[5]
    category_id = sys.argv[6]
    marks = sys.argv[7]
    grading_scale_id = sys.argv[8]
    section = sys.argv[9]

    new_grade = q.post_assignment_with_grades(section, assign_name,
                                              assign_date, total_possible,
                                              category_id, grading_scale_id,
                                              grades_date)
    qs.logger.info({"section": section, "grade": section_data['grades_data']})


if __name__ == '__main__':
    main()
