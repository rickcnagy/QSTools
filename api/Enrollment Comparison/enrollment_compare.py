#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import json

term_1_file = 'term 1 enrollment.json'
term_2_file = 'term 2 enrollment.json'


def main():
    term_1 = json.load(open(term_1_file))
    term_2 = json.load(open(term_2_file))
    
    print term_1 == term_2
    
    # for student, vals in term_1.iteritems():
#         subjects = vals['subjects']
#         if subjects != term_2[student]['subjects']:
#             print student
    

if __name__ == '__main__':
    main()