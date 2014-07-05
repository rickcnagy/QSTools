#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv
import json
import os
from collections import OrderedDict

"""Convenience static methods that don't require a CSV object"""

def p(obj):
    print json.dumps(obj, indent=4)

def write_csv(rows, filepath, keys=None, flatten_delim=' | '):
    """Save a dict to CSV with header rows, ordered keys, flattened vals, etc"""
    keys = keys or rows[0].keys()

    def flatten_val(val, delim):
        if type(val) is list:
            val = delim.join([str(i) for i in val])
        return val

    flattened_rows = [
        {key: flatten_val(val, flatten_delim)
            for key, val in row.iteritems()}
        for row in rows]

    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        for row in flattened_rows:
            writer.writerow(row)
        return


def dict_to_csv(data_dict, cols):
    """Take a data dict and write it to disk as a CSV.
    Can then be opened up as a CSV obj.

    Args:
        cols: columns to write to CSV. Each level of dict should be a column
    """
    # TODO: implement. Essentially is the reverse of CSV.as_tree()


"""Classes for actually working with CSVs"""


class CSV(object):
    """
    class for reading/writing CSV objects
    can work standalone or as the backbone for CSVMatch
    each row is a dictionary, and the values must be a string or list
    if it's a list, it will be flattened to a single cell with .flatten() upon save
    the delimeter is .delim
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.values = []
        self.cols = []
        self.cleaned_values = []
        self.rows = []
        self.cleaned_rows = []
        self.clean_func = None
        self.filter_func = None
        self.flatten_delim = ':'

        self.read()

    def read(self):
        """
        use val_funct to operate on all the values before as they are read in
        process must return something - to leave as is, return val
        """
        with open(self.filepath, 'rU') as f:
            self.cols = csv.reader(f).next()
            f.seek(0)
            raw_csv = csv.DictReader(f)
            for row in raw_csv:
                self.rows.append(row)
                self.values += row.values()
                if self.clean_func:
                    cleaned_row = {
                        key: self.clean_func(key, val)
                        for key, val
                        in row.iteritems()
                    }
                    self.cleaned_rows.append(cleaned_row)
                    self.cleaned_values += cleaned_row.values()
            return

    def save(self, overwrite=False, filepath=None):
        if not overwrite and not filepath:
            original = os.path.splitext(self.filepath)
            filepath = original[0] + ' - modified' + original[1]
        elif not filepath:
            filepath = self.filepath
        write_csv(self.rows, filepath, keys=self.cols, flatten_delim=self.flatten_delim)

    def as_tree(self, cols=None, rows_key='_rows'):
        """return a version of the rows as a tree
        format:
        Name | Subject | Grade
        -->
        {'Name': {'Subject': Grade}}
        """
        cols = cols or self.cols

        def process_branch(current, col_index):
            """recursively process a branch all the way to the leaves
            args:
            current         -- the current node to add nodes to, sibling to _row
            col_index       -- the index in cols that children will be from
            rows_key        -- the key in current that holds all the valid rows
            """
            rows = current[rows_key]
            col = cols[col_index]
            current.update(child_dict(rows, col))

            for key, new_current in current.iteritems():
                if key == rows_key: continue

                new_col_index = col_index + 1
                new_col = cols[new_col_index]
                if new_col_index == len(cols) - 1:
                    process_leaf(current, key, col, new_col)
                else:
                    process_branch(new_current, new_col_index)

            del current[rows_key]

        def child_dict(rows, col):
            """make a dict from rows, with dict for each key in the column
            the value of each key is the rows in rows that have the same val in col as the key"""
            return {
                row[col]: {rows_key: [
                    child
                    for child in rows
                    if child[col] == row[col]]}
                for row in rows
            }

        def process_leaf(current, key, node_col, leaf_col):
            matching_vals = [
                row[leaf_col]
                for row in current[rows_key]
                if leaf_col in row and row[node_col] == key
            ]
            matching_vals = list(set(matching_vals))
            if len(matching_vals) == 1:
                matching_vals = matching_vals[0]
            elif len(matching_vals) == 0:
                print "Warning: leaf is empty:\n{}".format(current[rows_key])
            else:
                print "Warning: leaf is list:\n{}".format(current[rows_key])
            current[key] = matching_vals

        root = child_dict(self.rows, cols[0])
        for _, new_current in root.iteritems():
            process_branch(new_current, 1)
        return root

    def unique(self, seq):
        return list(OrderedDict.fromkeys(seq))

    def cleaned_for_row(self, row):
        return self.cleaned_rows[self.rows.index(row)]

    def row_for_cleaned(self, cleaned):
        return self.rows[self.cleaned_rows.index(cleaned)]

    def __str__(self):
        return self.json()

    def __iter__(self):
        """iterating returns each row, one at a time"""
        return iter(self.rows)

    def json(self):
        return json.dumps(self.rows, indent=4)

    def dump_json(self, filename):
        json.dump(self.rows, open(filename, 'w'), indent=4)


class CSVMatch(CSV):

    def row_for_key_val(self, key, val, use_cleaned=False):
        """
        returns a list of matching rows
        args
            key: the column name on the CSV
            value: the value to match in that column
            use_cleaned: match using the cleaned list.
                 note: still returns the raw data, not the cleaned data

        if there are multiple matches:
            returns the first match
            raises MultipleMatchError
        """

        # TODO: This doesn't work right now, copy from row_for_val
        values = self.values
        rows = self.rows
        if use_cleaned:
            values = self.cleaned_values
            rows = self.cleaned_rows

        if (not val) or (not val in values): return

        match = None
        for row in rows:
            if row[key] == val:
                match = row
                if match:
                    raise MultipleMatchError()
                if use_cleaned:
                    match = self.row_for_cleaned(match)
        return match

    def row_for_val(self, val, use_cleaned=False, multiple_ok=False):
        """
        same as row_for_key_val, but searches all columns
        args:
            multiple_ok
                will return a list if there are multiple matches
                otherwise raise a ValueError
        """
        values = self.cleaned_values if use_cleaned else self.values
        rows = self.cleaned_rows if use_cleaned else self.rows

        if (not val) or (not val in values): return

        matches = [
            row for row
            in rows
            if val in row.values()
        ]

        if use_cleaned:
            matches = [self.row_for_cleaned(cleaned) for cleaned in matches]

        if len(matches) > 1:
            if multiple_ok:
                return matches
            else:
                raise ValueError(
                    "Multiple matches for value: {}\nmatches: {}".format(
                        val,
                        matches
                    ))
        return matches[0]

    def row_for_object(self, match_function, object):
        """
        like row_for_value, but allows for a more complicated match.
        match_function takes three parameters (vals, row, object) and returns true/false
        """
        for row in self.rows:
            if match_function(row, object):
                return row


class MultipleMatchError(Exception):

    def __init__(self, val, matches):
        self.val = val
        self.matches = matches

    def __str__(self):
        return "Multiple matches for value: {}\nmatches: {}".format(
            self.val,
            self.matches
            )

    pass
