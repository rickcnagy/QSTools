#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""Module for converting CSV's to JSONArray's of Row objects.
Usage is as follows:
./csv2json.py {filepath1} {filepath2} {...}
"""

import sys
import qs


def main():
    for filepath in sys.argv[1:]:
        csv = qs.CSV(filepath)
        new_filepath = filepath.replace('csv', 'json')
        json_filepath = csv.save_as_json(new_filepath)
        print "Saved {} as a JSON file:\n{}".format(filepath, json_filepath)

if __name__ == '__main__':
    main()
