"""
    Test of _get_list_diff function
"""

from pydeepdiff.diff import _get_list_diff


def test_empty_lists():
    diff = []
    diff.extend(_get_list_diff([], [], p_complex_details=True))

    assert not diff


def test_dic_lists():
    diff = []

    list_a = [{'field_1': 'id1', 'field_2': 'vala1'}, {'field_1': 'id2', 'field_2': 'vala2'}]
    list_b = [{'field_1': 'id3', 'field_2': 'valb1'}, {'field_1': 'id1', 'field_2': 'valb2'}]

    diff.extend(_get_list_diff(list_a, list_b, p_complex_details=True))

    assert diff
