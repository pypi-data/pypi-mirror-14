"""
    Helper library for QAL diff operations.
     
    :copyright: Copyright 2010-2014 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details. 

"""

import difflib

# General diffutils


def diff_strings(_a, _b):
    result = "---------- String A-----------\n"
    result += _a + "\n"
    result += "---------- String B-----------\n"
    result += _b + "\n"

    result += "---------- Diff between A and B-----------\n" + "\n"
    for line in difflib.context_diff(_a, _b):
        result += line

    return result


def diff_files(_file_a, _file_b):
    _f_a = open(_file_a, "r")
    _f_b = open(_file_b, "r")
    _a = _f_a.read()
    _b = _f_b.read()
    _f_a.close()
    _f_b.close()

    return diff_strings(_a=_a, _b=_b)


def cmp_key_columns(_left, _right, _key_columns):
    """
    This functions compares the columns in the specified key fields only and returns data usable in a </=/>-comparer
    """
    for _curr_key_column in _key_columns:

        if _left[_curr_key_column] < _right[_curr_key_column]:
            return -1
        elif _left[_curr_key_column] > _right[_curr_key_column]:
            return 1

    return 0


def match_all_columns(_left, _right):
    """Match all columns in two arrays, return false if they differ anywhere.
    
    :param array _left: The left array
    :param array _right: The right array
    
    .. note::
        This function is a *little bit* tailored to QAL needs. 
        The left column *has* to be used for column iteration, since _right might have extra columns for references
        to underlying structures that should not be compared.
    """

    # TODO: Check if this can be done more pythonically
    for _curr_column in range(0, len(_left)):
        if _left[_curr_column] != _right[_curr_column]:
            return False

    return True


def compare(_left, _right, _key_columns, _full):
    """ The compare function takes two structurally identical 2-dimensional matrices,
        _left and _right, matches them using the columns in _key_colums,
        and returns a tuple of the results.
        
        :param 2d-array _left: The left matrix
        :param 2d-array _right: The right matrix
        :param array _key_columns: An array with the key columns
        :param bool _full: If the _full parameter is True, also the values in the rows are compared, and the third \
        result, _different is populated with a list of rows where the values differ.
        
        
        :return array _missing_left: rows present in _right, but not in _left
        :return array _missing_right: rows present in _left, but not in _right
        :return array _difference: rows that by keys are present in _left and _right, but differ with in rows
        :return 2d-array _right_s: The _right matrix, but sorted by keys, often useful when one wants to continue \
            massaging the data.
        
        .. note::
            The results are not in original order, but sorted by their keys.
    """
    _missing_left = []
    _missing_right = []
    _difference = []

    # Order _left and _right using key columns
    try:
        if len(_key_columns) == 1:
            _left_s = sorted(_left, key=lambda d: (d[_key_columns[0]]))
            _right_s = sorted(_right, key=lambda d: (d[_key_columns[0]]))
        elif len(_key_columns) == 2:
            _left_s = sorted(_left, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]]))
            _right_s = sorted(_right, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]]))
        elif len(_key_columns) == 3:
            _left_s = sorted(_left, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]], d[_key_columns[2]]))
            _right_s = sorted(_right, key=lambda d: (d[_key_columns[0]], d[_key_columns[1]], d[_key_columns[2]]))
        elif len(_key_columns) == 0:
            raise Exception("Error in compare, at least one key column is required.")
        else:
            raise Exception("Err..sorry, only 3 key columns are supported currently, too tired to make it dynamic. :-)")
    except TypeError as e:
        if str(e).find("TypeError: unorderable types"):
            raise Exception("There seem to be data of different types in the same column.\n"
                            "Perhaps data need to be cast to some common data type, for example string. \n"
                            "Error:" + str(e))
        else:
            raise Exception(str(e))

    # From top, loop data sets, compare all rows
    _left_idx = _right_idx = 0
    _left_len = len(_left_s)
    _right_len = len(_right_s)
    while _left_idx < _left_len and _right_idx < _right_len:
        # print("_left_idx :" + str(_left_idx) + " value: "+str(_left_s[_left_idx][_key_columns[0]]) +
        # " | _right_idx : "  + str(_right_idx)+ " value: "+str(_right_s[_right_idx][_key_columns[0]]))
        _cmp_res = cmp_key_columns(_left_s[_left_idx], _right_s[_right_idx], _key_columns)
        # print("_cmp_res :" + str(_cmp_res))
        if _cmp_res < 0:
            # print("_missing_right.append " + str(_left_s[_left_idx]))
            _missing_right.append([_left_idx, _right_idx, _left_s[_left_idx]])
            _left_idx += 1
        elif _cmp_res > 0:
            # print("_missing_left.append " + str(_right_s[_right_idx]))
            _missing_left.append([_left_idx, _right_idx, _right_s[_right_idx]])
            _right_idx += 1
        else:
            # Keys are the same and _full is set, check all data 

            if _full is True and match_all_columns(_left_s[_left_idx], _right_s[_right_idx]) is not True:
                # Differing columns found, add _row to _difference
                _difference.append([_left_idx, _right_idx, _left_s[_left_idx], _right_s[_right_idx]])
            _left_idx += 1
            _right_idx += 1

    # Add remainders to missing
    if _left_idx < _left_len:
        for _curr_item in _left_s[_left_idx: _left_len]:
            # print("_missing_right.append (post) " + str([_left_idx, len(_missing_right) + 1, _curr_item]))
            _missing_right.append([_left_idx, _left_idx, _curr_item])

    if _right_idx < _right_len:
        for _curr_item in _right_s[_right_idx: _right_len]:
            # print("_missing_left.append (post)" + str([len(_missing_left) + 1, _right_idx,_curr_item]))
            _missing_left.append([_right_idx, _right_idx, _curr_item])

    return _missing_left, _missing_right, _difference, _right_s


# noinspection PyUnusedLocal
def diff_to_text(_missing_left, _missing_right, _different):
    """Creates a textual representation of the differences
    
        .. note::
            Not implemented.
    
    """
    _diff_text = ""

    raise Exception("diff_to_text is not implemented")


"""
A dictionary difference calculator
Originally posted as:
http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary/1165552#1165552
"""


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values

    """

    def __init__(self, current_dict, past_dict):
        """
        Compares two dicts

        :param current_dict: The correct dict
        :param past_dict: The old dict

        """

        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [
            set(d.keys()) for d in (current_dict, past_dict)
        ]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        """
        A list of added items

        """
        return self.current_keys - self.intersect

    def removed(self):
        """
        Returns a list of removed items

        """
        return self.past_keys - self.intersect

    def changed(self):
        """
        Returns a list of changed items

        """
        return set(o for o in self.intersect
                   if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """
        Returns a list of unchanged items

        """
        return set(o for o in self.intersect
                   if self.past_dict[o] == self.current_dict[o])

    @staticmethod
    def compare_documents(_old, _new):
        # TODO: This must probably be using field xpaths or something. JSON XPaths might be useful
        # The problem is if a field is in a list of objects. Then fieldId will not be unique in the list of objects.
        # How about always using xpaths for a change? The problem is fieldIds in lists.
        _changes = []
        _differ = DictDiffer(_new, _old)
        for _property in _differ.added():
            _changes.append({"action": "added", "attribute": _property, "before": None, "after": _new[_property]})

        for _property in _differ.removed():
            _changes.append({"action": "removed", "attribute": _property, "before": _old[_property], "after": None})

        for _property in _differ.changed():
            _changes.append({"action": "changed", "attribute": _property, "before": _old[_property], "after": _new[_property]})

        return _changes

    @staticmethod
    def pretty_print_diff(_changes):
        for _curr_diff in _changes:
            print("Attribute : " + str(_curr_diff["attribute"]) + ", action : " +  str(_curr_diff["action"]) +
                  "\nBefore : " + str(_curr_diff["before"]) + "\nAfter :  " + str(_curr_diff["after"]))
