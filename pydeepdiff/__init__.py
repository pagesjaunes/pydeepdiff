"""
    This package allows to compute deep differences between two python dictionnaries

    Differences are stored in the following format :

    lhs stands for Left Hand Side
    rhs stands for Right Hand Side

    - Creation : {'path':path_to_object,'kind':'N','rhs':value}
    - Deletion : {'path':path_to_object,'kind':'D','lhs':value}
    - Edition  : {'path':path_to_object,'kind':'E','lhs':value,'rhs':value}
    - Lists
        - Creation : {'path':path_to_object,'kind':'N','rhs_idx':index,'rhs':value}
        - Deletion : {'path':path_to_object,'kind':'D','lhs_idx':index,'lhs':value}
        - Move     : {'path':path_to_object,'kind':'M','lhs_idx':index,'rhs_idx':index}

    Example of use :

    from pydeepdiff.diff import get_diff

        dict_a = {'field_1': 'id1', 'field_2': 'vala1'}
        dict_b = {'field_1': 'id3', 'field_2': 'valb1'}

        differences = get_diff(dict_a, dict_b)

        # Differences contains one difference :
            [
                {
                    'path': [
                        'field_1'
                    ],
                    'kind': 'E',
                    'lhs': 'id1',
                    'rhs': 'id3'
                },
                {
                    'path': [
                        'field_2'
                    ],
                    'kind': 'E',
                    'lhs': 'vala1',
                    'rhs': 'valb1'
                }
            ]


        dict_a = {'id': '1', 'bloc': {'act': '1'}}
        dict_b = {'id': '1', 'bloc': {'act': '2'}}

        differences = get_diff(dict_a, dict_b))

        # Differences contains one difference :
            [
                {
                    'path': [
                        'bloc',
                        'act'
                    ],
                    'kind': 'E',
                    'lhs': '1',
                    'rhs': '2'
                }
            ]
"""

__version__ = "1.0.1"
