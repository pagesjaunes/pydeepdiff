pydiff
========

# Description

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

# Requirements
This lib requires python 3.2+

# Example of use

```python

    from pydiff.diff import get_diff

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
```

# Ignored fields

It is possible to ignore some fields when comparing objects.
For this, pass a list of these fields to the comparison function.

Example : don't compare the field 'act' of the nested 'bloc' object :

```python

    dict_a = {'id': '1', 'bloc': {'act': '1'}}
    dict_b = {'id': '1', 'bloc': {'act': '2'}}

    diff = get_diff(dict_a, dict_b, 'root', {}, ['root.bloc.act'])
```

In this example the result is an empty list of differences.

# Specific mapping

When comparing two list of dict, we have to "associate" each item of the left side list to an item of the right side list.
For this, we have to know "HOW" making this association : often a dict will have a field that represents its id, and we want to use it.
In pydiff, this case is resolved with a mapping file.

In the following example, we explicitly use the 'field_1' to identify an object of the list.

```python

    list_a = [{'field_1': 'id1', 'field_2': 'vala1'}, {'field_1': 'id2', 'field_2': 'vala2'}]
    list_b = [{'field_1': 'id3', 'field_2': 'valb1'}, {'field_1': 'id1', 'field_2': 'valb2'}]

    mapping = {'root': 'field_1'}

    diff = _get_list_dict_diff(list_a, list_b, 'root', mapping, p_complex_details=True)
```

Note that you will have to use the same string to represent the root object in the path and in the mapping dictionnary (here we use 'root').

The result is the following list of differences :

```
    [
        {'path_to_object': 'root', 'filter': 'root', 'rhs_idx': 1, 'lhs_idx': 0, 'kind': 'M'},
        {'rhs': 'valb2', 'lhs': 'vala1', 'kind': 'E', 'path_to_object': 'root.[0].field_2', 'filter': 'root.field_2'},
        {'lhs_idx': 1, 'kind': 'D', 'lhs': {'field_2': 'vala2', 'field_1': 'id2'}, 'path_to_object': 'root', 'filter': 'root'},
        {'rhs_idx': 0, 'kind': 'N', 'rhs': {'field_2': 'valb1', 'field_1': 'id3'}, 'path_to_object': 'root', 'filter': 'root'}
    ]
```

# Tests

To launch unit tests, just run this command from the project home directory (you will need py.test installed)

```
py.test test

```
