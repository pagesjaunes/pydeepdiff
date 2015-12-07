"""
    Test of get_id_from_mapping function
"""

from pydeepdiff.diff import _get_id_from_mapping


def test_basic():
    mapping = [{'path': '', 'id': 'field_1'}]
    path = ''
    field = _get_id_from_mapping(mapping, path)

    assert field == 'field_1'


def test_empty():
    mapping = []
    path = ''
    field = _get_id_from_mapping(mapping, path)

    assert field is None
