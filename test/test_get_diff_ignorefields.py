"""
    Test of ignore fields
"""

from pydiff.diff import get_diff


def test_basic():
    diff = []

    dict_a = {'field_1': 'id1', 'field_2': 'vala1'}
    dict_b = {'field_1': 'id3', 'field_2': 'valb1'}

    diff.extend(get_diff(dict_a, dict_b, ['root'], {}, ['root.field_1']))

    expected_diff = [{'path': ['root', 'field_2'], 'kind': 'E', 'lhs': 'vala1', 'rhs': 'valb1'}]

    assert diff == expected_diff


def test_nested():
    diff = []

    dict_a = {'id': '1', 'bloc': {'act': '1'}}
    dict_b = {'id': '1', 'bloc': {'act': '2'}}

    diff.extend(get_diff(dict_a, dict_b, ['root'], {}, ['root.bloc.act']))

    expected_diff = []

    assert diff == expected_diff