"""
    Test of ignore fields
"""

from pydeepdiff.diff import get_diff


def test_basic():
    diff = []

    dict_a = {'field_1': 'id1', 'field_2': 'vala1'}
    dict_b = {'field_1': 'id3', 'field_2': 'valb1'}

    diff.extend(get_diff(dict_a, dict_b, '', {}, ['field_1'], p_complex_details=True))

    expected_diff = [{'path_to_object': 'field_2', 'filter': 'field_2', 'kind': 'E', 'lhs': 'vala1', 'rhs': 'valb1'}]

    assert diff == expected_diff


def test_nested():
    diff = []

    dict_a = {'id': '1', 'bloc': {'act': '1'}}
    dict_b = {'id': '1', 'bloc': {'act': '2'}}

    diff.extend(get_diff(dict_a, dict_b, '', {}, ['bloc.act'], p_complex_details=True))

    expected_diff = []

    assert diff == expected_diff
