"""
    Test of _get_dictionary_diff function
"""

from pydiff.diff import _get_dictionary_diff


def test_empty_dict():
    diff = []
    diff.extend(_get_dictionary_diff({}, {}))

    assert not diff


def test_basic():
    diff = []

    dict_a = {'field_1': 'id1', 'field_2': 'vala1'}
    dict_b = {'field_1': 'id3', 'field_2': 'valb1'}

    diff.extend(_get_dictionary_diff(dict_a, dict_b))

    expected_diff = [{'path': ['field_1'], 'kind':'E', 'lhs':'id1', 'rhs':'id3'}, {'path': ['field_2'], 'kind':'E', 'lhs':'vala1', 'rhs':'valb1'}]

    assert diff == expected_diff


def test_nested():
    diff = []

    dict_a = {'id': '1', 'bloc': {'act': '1'}}
    dict_b = {'id': '1', 'bloc': {'act': '2'}}

    diff.extend(_get_dictionary_diff(dict_a, dict_b))

    expected_diff = [{'path': ['bloc', 'act'], 'kind':'E', 'lhs':'1', 'rhs':'2'}]

    assert diff == expected_diff
