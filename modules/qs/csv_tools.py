#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv
import json
import os
from collections import OrderedDict
import qs

FLATTEN_DELIM = ','


# ==============================================================
# = Convenience static methods that don't require a CSV object =
# ==============================================================


def write_csv(rows, filepath, overwrite=False, column_headers=None):
    """Write a CSV to disk.

    Takes a list of dicts, where keys map to columns, and values map to row
    cells.

    If a key exists in any dict, it'll be added to the CSV headers, so in
    general all dicts should have the same keys.

    By default, the column headers will be alphabetically sorted.

    To specify custom column headers/sorting, supply the column_headers arg

    By default, the filepath is made unique using the default behavior of
    qs.unique_path.

    Args:
        rows: a list of dicts, each dict corresponding to a single row in the
            CSV.
        filepath: path to write the CSV to
        overwrite: by default, this function finds a unique file path based
            on the filepath supplied. To overwrite the file at that path,
            set overwrite to True
        column_headers: Supply a list of column headers to use in the CSV. This
            is useful both for order and for specifying a specific subset of
            headers to use instead of all keys in the rows array.
    """
    filepath = os.path.expanduser(filepath)

    if column_headers is None:
        column_headers = set()
        for row in rows:
            column_headers.update(row.keys())
        column_headers = sorted(list(column_headers))

    if overwrite is False:
        filepath = qs.unique_path(filepath)

    for row in rows:
        _clean_row_for_csv(row)

    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, column_headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def dict_to_csv(data_dict, cols):
    """Take a data dict and write it to disk as a CSV.
    Can then be opened up as a CSV obj.

    Args:
        cols: columns to write to CSV. Each level of dict should be a column
    """
    # TODO: implement. Essentially is the reverse of CSV.as_tree()


def _clean_row_for_csv(row):
    for key, val in row.iteritems():
        if type(val) is list:
            row[key] = FLATTEN_DELIM.join([str(i for i in val)])
        elif type(val) is not str:
            row[key] = str(val)
    return row

# ===============
# = CSV Classes =
# ===============


class CSV(object):
    """
    Class for reading/writing CSV objects.

    Can work standalone or as the backbone for CSVMatch.

    Each row is a dictionary.
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
            return True

    def save(self, overwrite=False):
        """Save the CSV to disk."""
        write_csv(
            self.rows,
            self.filepath,
            overwrite=overwrite,
            column_headers=self.cols
        )

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
                current: the current node to add nodes to, sibling to _row
                col_index: the index in cols that children will be from
                rows_key: the key in current that holds all the valid rows
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

            the value of each key is the rows in rows that have the same val in
            col as the key
            """
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

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        return self.rows[index]

    def json(self):
        return json.dumps(self.rows, indent=4)

    def dump_json(self, filename):
        json.dump(self.rows, open(filename, 'w'), indent=4, sort_keys=True)


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

        if not val or val not in values: return

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

        if not val or val not in values: return

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
                        qs.dumps(matches)
                    ))
        return matches[0]

    def row_for_object(self, match_function, object):
        """
        like row_for_value, but allows for a more complicated match.

        match_function takes three parameters (vals, row, object) and returns
        true/false
        """
        for row in self.rows:
            if match_function(row, object):
                return row


class MultipleMatchError(Exception):

    def __init__(self, val, matches):
        self.val = val
        self.matches = matches

    def __str__(self):
        return "Multiple matches for value: {}\nmatches:{}".format(
            self.val,
            qs.dumps(self.matches))
