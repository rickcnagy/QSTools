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
        filepath = qs.unique_path(filepath, extension='csv')

    for row in rows:
        _sanitized_row_for_csv(row)

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


def _sanitized_row_for_csv(row):
    for key, val in row.iteritems():
        if not val:
            row[key] = ''
        elif type(val) is list:
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

    Each row is a dictionary, and self.cols is the correctly ordered list of
    columns.

    Empty rows are removed.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.values = []
        self.cols = []
        self.rows = []
        self.filter_func = None
        self.flatten_delim = ':'

        self.read()

    def read(self):
        with open(self.filepath, 'rU') as f:
            self.cols = csv.reader(f).next()
            f.seek(0)
            raw_csv = csv.DictReader(f)

            for row in raw_csv:
                if not any(v for k, v in row.iteritems()):
                    continue

                row = {
                    self._sanitized(key): self._sanitized(val)
                    for key, val in row.iteritems()
                }
                self.rows.append(row)
                self.values += row.values()

            return True

    def save(self, filepath=None, overwrite=False):
        """Save the CSV to disk. Returns the filepath of the saved file."""
        self._prepare_for_saving()
        output_filepath = self._get_output_filepath(
            filepath,
            overwrite,
            'csv')

        write_csv(
            self.rows,
            output_filepath,
            overwrite=True,
            column_headers=self.cols
        )
        return output_filepath

    def save_as_json(self, filepath=None, overwrite=False):
        """Save the CSV as a JSON object. Returns the filepath of the file."""
        self._prepare_for_saving()
        output_filepath = self._get_output_filepath(
            filepath,
            overwrite,
            'json')

        qs.write(self.get_json(), output_filepath)
        return output_filepath

    def get_json(self):
        return qs.dumps(self.rows)

    def _sanitized(self, key):
        if not isinstance(key, basestring):
            return key
        if isinstance(key, unicode):
            return key
        elif key:
            return qs.unicode_decode(key)
        else:
            return None

    def _prepare_for_saving(self):
        """Processes the rows for saving"""
        for row in self.rows:
            new_cols = {i for i in row.keys() if i not in self.cols}
            self.cols.extend(new_cols)
        return True

    def _get_output_filepath(self, filepath, overwrite, new_extension):
        filepath = filepath or self.filepath
        original_extension = os.path.splitext(self.filepath)[1]
        if overwrite:
            return self.filepath.replace(original_extension, new_extension)
        else:
            return qs.unique_path(self.filepath, extension=new_extension)

    def __str__(self):
        return self.json()

    def __iter__(self):
        """iterating returns each row, one at a time"""
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        return self.rows[index]


class CSVFromJSONFile(CSV):

    def read(self):
        data = self._get_json()
        self.cols = data[0].keys()

        for row in data:
            row = {
                self._sanitized(key): self._sanitized(val)
                for key, val in row.iteritems()
            }
            self.rows.append(row)
            self.values += row.values()

        return True

    def _get_json(self):
        with open(self.filepath, 'rU') as f:
            return json.load(f)


class CSVFromRowList(CSVFromJSONFile):

    def __init__(self, row_list, output_filepath):
        self.row_list = row_list
        self.output_filepath = output_filepath

        super(CSVFromRowList, self).__init__(None)

    def _get_json(self):
        return self.row_list

    def _get_output_filepath(self, filepath, overwrite, new_extension):
        return self.output_filepath


class CSVTree(CSV):
    """A CSV that we want to convert to a dict tree via .tree()

    The format:
    Name | Subject | Grade
    -->
    {'Name': {'Subject': Grade}}
    """

    def tree(self, cols=None, rows_key='_rows'):
        cols = cols or self.cols

        root = self._child_dict(self.rows, cols[0])
        for _, new_current in root.iteritems():
            self._process_branch(new_current, 1)
        return root

    def _child_dict(rows, col):
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

    def _process_branch(current, col_index):
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

    def _process_leaf(current, key, node_col, leaf_col):
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


class CSVMatch(CSV):

    def row_for_key_val(self, key, val, use_sanitized=False):
        """
        returns a list of matching rows
        args
            key: the column name on the CSV
            value: the value to match in that column
            use_sanitized: match using the cleaned list.
                 note: still returns the raw data, not the cleaned data

        if there are multiple matches:
            returns the first match
            raises MultipleMatchError
        """

        # TODO: This doesn't work right now, copy from row_for_val
        values = self.values
        rows = self.rows
        if use_sanitized:
            values = self.cleaned_values
            rows = self.cleaned_rows

        if not val or val not in values: return

        match = None
        for row in rows:
            if row[key] == val:
                match = row
                if match:
                    raise MultipleMatchError()
                if use_sanitized:
                    match = self.row_for_sanitizeded(match)
        return match

    def row_for_val(self, val, use_sanitized=False, multiple_ok=False):
        """
        same as row_for_key_val, but searches all columns
        args:
            multiple_ok
                will return a list if there are multiple matches
                otherwise raise a ValueError
        """
        values = self.cleaned_values if use_sanitized else self.values
        rows = self.cleaned_rows if use_sanitized else self.rows

        if not val or val not in values: return

        matches = [
            row for row
            in rows
            if val in row.values()
        ]

        if use_sanitized:
            matches = [
                self.row_for_sanitizeded(cleaned)
                for cleaned in matches
            ]

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
