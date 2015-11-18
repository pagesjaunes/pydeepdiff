"""
    Test of _get_list_dict_diff function
"""

from pydiff.diff import _get_list_dict_diff


def test_empty_lists():
    diff = []
    diff.extend(_get_list_dict_diff([{}], [{}]))

    assert not diff


def test_no_mapping_lists():
    """ No mapping = compute positionnal diff """
    diff = []

    list_a = [{'field_1': 'id1', 'field_2': 'vala1'}, {'field_1': 'id2', 'field_2': 'vala2'}]
    list_b = [{'field_1': 'id3', 'field_2': 'valb1'}, {'field_1': 'id1', 'field_2': 'valb2'}]

    diff.extend(_get_list_dict_diff(list_a, list_b))

    expected_diff = [
                     {'rhs': 'id3', 'lhs': 'id1', 'kind': 'E', 'path': ['field_1']},
                     {'rhs': 'valb1', 'lhs': 'vala1', 'kind': 'E', 'path': ['field_2']},
                     {'rhs': 'id1', 'lhs': 'id2', 'kind': 'E', 'path': ['field_1']},
                     {'rhs': 'valb2', 'lhs': 'vala2', 'kind': 'E', 'path': ['field_2']}
                     ]

    assert diff == expected_diff


def test_mapping_lists():
    diff = []

    list_a = [{'field_1': 'id1', 'field_2': 'vala1'}, {'field_1': 'id2', 'field_2': 'vala2'}]
    list_b = [{'field_1': 'id3', 'field_2': 'valb1'}, {'field_1': 'id1', 'field_2': 'valb2'}]

    mapping = {'root': 'field_1'}

    diff.extend(_get_list_dict_diff(list_a, list_b, ['root'], mapping))

    expected_diff = [
                     {'path': ['root'], 'rhs_idx':1, 'lhs_idx':0, 'kind': 'M'},
                     {'rhs': 'valb2', 'lhs': 'vala1', 'kind': 'E', 'path': ['root', '[0]', 'field_2']},
                     {'lhs_idx': 1, 'kind': 'D', 'lhs': {'field_2': 'vala2', 'field_1': 'id2'}, 'path': ['root']},
                     {'rhs_idx': 0, 'kind': 'N', 'rhs': {'field_2': 'valb1', 'field_1': 'id3'}, 'path': ['root']}
                     ]

    assert diff == expected_diff
