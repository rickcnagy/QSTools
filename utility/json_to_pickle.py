#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import pickle

input_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/INTVLA/INTVLA Grades to Upload.JSON'
pickle.dump(json.load(open(input_filename)), open(input_filename.replace('.JSON', '.p'), 'w'))
