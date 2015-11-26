"""
    Test of _get_simpletype_diff function
"""

from pydeepdiff.diff import _get_simpletype_diff


def test_no_diff():
    diff = []
    diff.extend(_get_simpletype_diff(5, 5))
    diff.extend(_get_simpletype_diff('5', '5'))

    assert not diff


def test_one_diff():
    diff = []
    diff.extend(_get_simpletype_diff(5, 4, p_details=True))

    expected_diff = [{'path_to_object': "", 'filter': "", 'kind': 'E', 'lhs': 5, 'rhs': 4}]

    assert diff == expected_diff


def test_none():
    diff = []
    diff.extend(_get_simpletype_diff(5, None))
    diff.extend(_get_simpletype_diff(None, 5))
    diff.extend(_get_simpletype_diff(None, None))

    assert len(diff) == 2
