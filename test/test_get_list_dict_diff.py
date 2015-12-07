"""
    Test of _get_list_dict_diff function
"""

from pydeepdiff.diff import _get_list_dict_diff


def test_empty_lists():
    diff = []
    diff.extend(_get_list_dict_diff([{}], [{}], p_complex_details=True))

    assert not diff


def test_no_mapping_lists():
    """ No mapping = compute positionnal diff """
    diff = []

    list_a = [{'field_1': 'id1', 'field_2': 'vala1'}, {'field_1': 'id2', 'field_2': 'vala2'}]
    list_b = [{'field_1': 'id3', 'field_2': 'valb1'}, {'field_1': 'id1', 'field_2': 'valb2'}]

    diff.extend(_get_list_dict_diff(list_a, list_b, p_complex_details=True))

    expected_diff = [
                     {'rhs': 'id3', 'lhs': 'id1', 'kind': 'E', 'path_to_object': 'field_1', 'filter': 'field_1'},
                     {'rhs': 'valb1', 'lhs': 'vala1', 'kind': 'E', 'path_to_object': 'field_2', 'filter': 'field_2'},
                     {'rhs': 'id1', 'lhs': 'id2', 'kind': 'E', 'path_to_object': 'field_1', 'filter': 'field_1'},
                     {'rhs': 'valb2', 'lhs': 'vala2', 'kind': 'E', 'path_to_object': 'field_2', 'filter': 'field_2'}
                     ]

    assert diff == expected_diff


def test_mapping_lists():
    diff = []

    list_a = [{'field_1': 'id1', 'field_2': 'vala1'}, {'field_1': 'id2', 'field_2': 'vala2'}]
    list_b = [{'field_1': 'id3', 'field_2': 'valb1'}, {'field_1': 'id1', 'field_2': 'valb2'}]

    mapping = [{'path': '', 'id': 'field_1'}]

    diff.extend(_get_list_dict_diff(list_a, list_b, '', mapping, p_complex_details=True))

    expected_diff = [
                        {'path_to_object': '', 'filter': '', 'rhs_idx': 1, 'lhs_idx': 0, 'kind': 'M'},
                        {'rhs': 'valb2', 'lhs': 'vala1', 'kind': 'E', 'path_to_object': '[0].field_2', 'filter': 'field_2'},
                        {'lhs_idx': 1, 'kind': 'D', 'lhs': {'field_2': 'vala2', 'field_1': 'id2'}, 'path_to_object': '', 'filter': ''},
                        {'rhs_idx': 0, 'kind': 'N', 'rhs': {'field_2': 'valb1', 'field_1': 'id3'}, 'path_to_object': '', 'filter': ''}
                    ]

    assert diff == expected_diff
