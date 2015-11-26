"""
    Test of _get_list_simple_diff function
"""

from pydeepdiff.diff import _get_list_simple_diff


def test_empty_lists():
    """ Two empty lists returns an empty diff """
    diff = []
    diff.extend(_get_list_simple_diff([], []))

    assert not diff


def test_int_lists():
    """ List of int """
    diff = []

    list_a = [1, 2, 3, 4]
    list_b = [3, 5, 1]

    diff.extend(_get_list_simple_diff(list_a, list_b, p_details=True))

    expected_diff = [
                     {'lhs_idx': 1, 'kind': 'D', 'lhs': 2, 'path_to_object': "", 'filter': ""},
                     {'lhs_idx': 3, 'kind': 'D', 'lhs': 4, 'path_to_object': "", 'filter': ""},
                     {'rhs_idx': 1, 'kind': 'N', 'rhs': 5, 'path_to_object': "", 'filter': ""}
                    ]

    assert diff == expected_diff


def test_int_equal_lists():
    """ No differences (order doesn't matter) """
    diff = []

    list_a = [1, 2, 3, 4]
    list_b = [3, 2, 1, 4]

    diff.extend(_get_list_simple_diff(list_a, list_b))

    assert not diff


def test_str_lists():
    """ Lists of string """
    diff = []

    list_a = ['1', '2', '3', '4']
    list_b = ['3', '5', '1']

    diff.extend(_get_list_simple_diff(list_a, list_b, p_details=True))

    expected_diff = [
                     {'lhs_idx': 1, 'kind': 'D', 'lhs': '2', 'path_to_object': "", 'filter': ""},
                     {'lhs_idx': 3, 'kind': 'D', 'lhs': '4', 'path_to_object': "", 'filter': ""},
                     {'rhs_idx': 1, 'kind': 'N', 'rhs': '5', 'path_to_object': "", 'filter': ""}
                    ]

    assert diff == expected_diff
