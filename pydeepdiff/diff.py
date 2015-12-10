"""
    Set of functions that handle differences between two objects
    Differences are stored in the following format :

    lhs stands for Left Hand Side
    rhs stands for Right Hand Side

    - Creation (N stands for New) : {'path_to_object':path_to_object,'kind':'N','rhs':value}
    - Deletion : {'path_to_object':path_to_object,'kind':'D','lhs':value}
    - Edition  : {'path_to_object':path_to_object,'kind':'E','lhs':value,'rhs':value}
    - Lists
        - Creation : {'path':path_to_object,'kind':'N','rhs_idx':index,'rhs':value}
        - Deletion : {'path':path_to_object,'kind':'D','lhs_idx':index,'lhs':value}
        - Move     : {'path':path_to_object,'kind':'M','lhs_idx':index,'rhs_idx':index}
"""

import logging
import re

logger = logging.getLogger("pydeepdiff")


def get_diff(p_lhs, p_rhs, p_path="", p_mapping=[], p_ignored_fields=[], p_simple_details=True, p_complex_details=False):
    """
        Compute difference between two objects

        p_lhs               Left Hand Side of the comparison
        p_rhs               Right Hand Side of the comparison
        p_path              Path associated to the difference (useful for nested objects comparison)
        p_mapping           A mapping list of dict that associates a json path to a field containing the object id {'path':'path.to.object','id':'fieldname'}
        p_ignored_fields    List of path that will not be compared
        p_simple_details    If true, retrieves the values of "simple types differences" (int, float, string)
                            It will give the value for each version (old or new) of a field that is of simple type (int, string)
        p_complex_details   If true, retrieves the values of "complex types differences" (list, dict)
    """
    current_diffs = []  # Computed diffs

    # Check if the current path belongs to the paths list to ignore for comparison
    no_idx_path = _get_path_without_indexes(p_path)
    if no_idx_path in p_ignored_fields:
        return []

    if not isinstance(p_lhs, type(p_rhs)):
        # If the type are different, it corresponds to a creation and a deletion
        diff = {'path_to_object': p_path, 'kind': 'D', 'filter': no_idx_path}
        if p_complex_details:
            diff['lhs'] = p_lhs
        current_diffs.append(diff)
        diff = {'path_to_object': p_path, 'kind': 'N', 'filter': no_idx_path}
        if p_complex_details:
            diff['rhs'] = p_rhs
        current_diffs.append(diff)
    elif isinstance(p_lhs, dict):
        # Dictionary data
        current_diffs.extend(_get_dictionary_diff(p_lhs, p_rhs, p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details))
    elif isinstance(p_lhs, list):
        # List data
        current_diffs.extend(_get_list_diff(p_lhs, p_rhs, p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details))
    else:
        # Simple data
        current_diffs.extend(_get_simpletype_diff(p_lhs, p_rhs, p_path, p_simple_details))

    return current_diffs


def _get_simpletype_diff(p_lst, p_rst, p_path="", p_details=True):
    """
        Generate a "E" diff if p_lst and p_rst are not equals

        p_lst       Left Simple Type
        p_rst       Right Simple Type
        p_path      The path of p_lst and p_rst if they "come" from a nested object
        p_details   If false, retrieves only the diff type, not the values

        return  A list of a single "diff" object if p_lst != p_rst, an empty one else
    """
    current_diffs = []

    if p_lst != p_rst:
        no_idx_path = _get_path_without_indexes(p_path)
        diff = {'path_to_object': p_path, 'kind': 'E', 'filter': no_idx_path}
        if p_details:
            diff['lhs'] = p_lst
            diff['rhs'] = p_rst
        current_diffs.append(diff)

    return current_diffs


def _get_dictionary_diff(p_ldic, p_rdic, p_path="", p_mapping=[], p_ignored_fields=[], p_simple_details=True, p_complex_details=False):
    """
        Generate diff between two dictionaries.
        Creates "N" type diff for each key present only on the right side
        Creates "D" type diff for each key present only on the left side
        Creates as differences as they are in the nested objects

        p_ldic              Left Dictionary
        p_rdic              Right Dictionary
        p_path              Path associated to the difference (useful for nested objects comparison)
        p_mapping           A mapping list of dict that associates a json path to a field containing the object id {'path':'path.to.object','id':'fieldname'}
        p_ignored_fields    List of path that will not be compared
        p_simple_details    If true, retrieves the values of "simple types differences" (int, float, string)
                            It will give the value for each version (old or new) of a field that is of simple type (int, string)
        p_complex_details   If true, retrieves the values of "complex types differences" (list, dict)

        return   A list of differences
    """
    current_diffs = []

    # Computes the intersection of their keys
    intersect = p_ldic.keys() & p_rdic.keys()

    # Sort the keys so as to be able to test on a given order
    intersect = sorted(intersect)

    # Additions
    for key in (p_ldic.keys() - intersect):
        # As the diff is on "key" field, we add it to the path
        current_path = _add_field_to_path(p_path, key)
        no_idx_path = _get_path_without_indexes(current_path)
        if no_idx_path not in p_ignored_fields:
            diff = {'path_to_object': current_path, 'kind': 'N', 'filter': no_idx_path}
            if p_complex_details:
                diff['rhs'] = p_ldic[key]
            current_diffs.append(diff)

    # Deletions
    for key in (p_rdic.keys() - intersect):
        # As the diff is on "key" field, we add it to the path
        current_path = _add_field_to_path(p_path, key)
        no_idx_path = _get_path_without_indexes(current_path)
        if no_idx_path not in p_ignored_fields:
            diff = {'path_to_object': current_path, 'kind': 'D', 'filter': no_idx_path}
            if p_complex_details:
                diff['lhs'] = p_rdic[key]
            current_diffs.append(diff)

    # Changes
    for key in intersect:
        # As the diff is on "key" field, we add it to the path
        current_path = _add_field_to_path(p_path, key)
        current_diffs.extend(get_diff(p_ldic.get(key), p_rdic.get(key), current_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details))

    return current_diffs


def _get_list_diff(p_llist, p_rlist, p_path="", p_mapping=[], p_ignored_fields=[], p_simple_details=True, p_complex_details=False):
    """
        Generate "A type" array diff

        p_llist             Left List
        p_rlist             Right List
        p_path              The path of p_llist and p_rlist if they "come" from a nested object
        p_mapping           A mapping list of dict that associates a json path to a fiel containing the object id {'path':'path.to.object','id':'fieldname'}
        p_ignored_fields    List of path that will not be compared
        p_simple_details    If true, retrieves the values of "simple types differences" (int, float, string)
                            It will give the value for each version (old or new) of a field that is of simple type (int, string)
        p_complex_details   If true, retrieves the values of "complex types differences" (list, dict)

        return  A list of diff (type "A" as 'Array').
    """
    current_diffs = []

    # Detect the items list type
    item_type = None
    item_type = _get_list_type(p_llist)
    if not item_type:
        item_type = _get_list_type(p_rlist)

    if item_type == "dict":
        current_diffs = _get_list_dict_diff(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details)
    elif item_type == "list":
        current_diffs = _get_list_diff_by_position(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details)
    else:
        current_diffs = _get_list_simple_diff(p_llist, p_rlist, p_path, p_simple_details)

    return current_diffs


def _get_list_type(p_list):
    """
        Return the type of the list items
        Note : check only the first item, and assume that the list is homogeneous

        p_list  A list

        return the type of the first item of the list, None if the list is empty
    """
    r_type = None

    if p_list:
        if isinstance(p_list[0], dict):
            r_type = 'dict'
        elif isinstance(p_list[0], list):
            r_type = 'list'

    return r_type


def _get_list_simple_diff(p_llist, p_rlist, p_path="", p_details=False):
    """
        Compute the diff between two lists containing simple type items

        p_llist     Left List containing simple type items
        p_rlist     Right List containing simple type items
        p_path      The path of p_llist and p_rlist if they "come" from a nested object
        p_details   If false, retrieves only the diff type, not the values

        return  A list of diff (type "A" as 'Array').
    """
    current_diffs = []
    no_idx_path = _get_path_without_indexes(p_path)

    # Deleted items
    if p_details:
        left_not_in_right = [{'path_to_object': p_path, 'kind': 'D', 'filter': no_idx_path, 'lhs_idx': left_index, 'lhs': left_item} for left_index, left_item in enumerate(p_llist, start=0) if left_item not in p_rlist]
    else:
        left_not_in_right = [{'path_to_object': p_path, 'kind': 'D', 'filter': no_idx_path} for left_index, left_item in enumerate(p_llist, start=0) if left_item not in p_rlist]

    # New items
    if p_details:
        right_not_in_left = [{'path_to_object': p_path, 'kind': 'N', 'filter': no_idx_path, 'rhs_idx': right_index, 'rhs': right_item} for right_index, right_item in enumerate(p_rlist, start=0) if right_item not in p_llist]
    else:
        right_not_in_left = [{'path_to_object': p_path, 'kind': 'N', 'filter': no_idx_path} for right_index, right_item in enumerate(p_rlist, start=0) if right_item not in p_llist]

    current_diffs.extend(left_not_in_right)
    current_diffs.extend(right_not_in_left)

    return current_diffs


def _get_list_dict_diff(p_llist, p_rlist, p_path="", p_mapping=[], p_ignored_fields=[], p_simple_details=True, p_complex_details=False):
    """
        Compute the diff between two lists containing dictionaries.
        Try to get a mapping from "p_mapping" to identify the fieldname that makes matchs possible
        If not fieldname can be gotten, a single "positionnal" diff is compute

        p_llist             Left dict List
        p_rlist             Right ditc List
        p_path              The path of p_llist and p_rlist if they "come" from a nested object
        p_mapping           A mapping list of dict that associates a json path to a field containing the object id {'path':'path.to.object','id':'fieldname'}
        p_ignored_fields    List of path that will not be compared
        p_simple_details    If true, retrieves the values of "simple types differences" (int, float, string)
                            It will give the value for each version (old or new) of a field that is of simple type (int, string)
        p_complex_details   If true, retrieves the values of "complex types differences" (list, dict)

        return  A list of diff (type "A" as 'Array') + a list of true diff between subobject
    """
    current_diffs = []

    # Any id_field defined for this path ?
    try:
        # As the path stores indexes, we have to remove them to match the mapping format
        no_idx_path = _get_path_without_indexes(p_path)
        logger.debug("id_fieldname from %s", no_idx_path)
        # id_fieldname = p_mapping[no_idx_path]
        id_fieldname = _get_id_from_mapping(p_mapping, no_idx_path)
        logger.debug("id_fieldname : %s", id_fieldname)
    except KeyError as e:
        # Can't compare elements by id, compare by position only
        logger.debug("No id_fieldname matching the path %s. Using positional comparaison for this list ...", no_idx_path)
        current_diffs = _get_list_diff_by_position(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details)
    except Exception as e:
        logger.debug("error getting id_fieldname")
        logger.error(e)
    else:
        if id_fieldname is None:
            logger.debug("No id_fieldname matching the path %s. Using positional comparaison for this list ...", no_idx_path)
            current_diffs = _get_list_diff_by_position(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details)
        else:
            logger.debug("Create indexes")

            # Stores indexes of objects that are not in the right list
            left_not_in_right = [x for x in range(len(p_llist))]

            # Stores indexes of objects that are not in the left list
            right_not_in_left = [x for x in range(len(p_rlist))]

            # Loop over left and right lists and :
            #   - compares objects that owns the same value for the id_fieldname
            #   - removes indexes of compared object from the left_not_in_right and right_not_in_left lists
            #
            # Not so pythonic ... but to much treatments to use a comprehensive list
            logger.debug("Loop on lists ...")

            for left_index, left_item in enumerate(p_llist, start=0):
                for right_index, right_item in enumerate(p_rlist, start=0):
                    if left_item.get(id_fieldname, None) == right_item.get(id_fieldname, None):
                        logger.debug("Compare left and right because %s == %s", left_item.get(id_fieldname, None), right_item.get(id_fieldname, None))

                        # Add a move diff if the item has moved
                        if left_index != right_index:
                            diff = {'path_to_object': p_path, 'kind': 'M', 'filter': no_idx_path}
                            if p_complex_details:
                                diff['lhs_idx'] = left_index
                                diff['rhs_idx'] = right_index
                            current_diffs.append(diff)

                        # We keep a trace of the list idx in the path
                        # Append the index of the element to the path
                        new_path = _add_field_to_path(p_path, "[{0}]".format(str(left_index)))
                        logger.debug(current_diffs)

                        current_diffs.extend(get_diff(left_item, right_item, new_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details))

                        logger.debug(current_diffs)

                        # left_not_in_right and right_not_in_left store index
                        left_not_in_right.remove(left_index)
                        right_not_in_left.remove(right_index)
                    else:
                        # Not "comparable" : each ones stay in the left_not_in_right and right_not_in_left lists for "D" and "N" diffs generation
                        logger.debug("Can't compare left and right : %s != %s", left_item.get(id_fieldname, None), right_item.get(id_fieldname, None))

            # Deleted items
            for i in left_not_in_right:
                diff = {'path_to_object': p_path, 'kind': 'D', 'filter': no_idx_path}
                if p_complex_details:
                    diff['lhs_idx'] = i
                    diff['lhs'] = p_llist[i]
                current_diffs.append(diff)

            # New items
            for i in right_not_in_left:
                diff = {'path_to_object': p_path, 'kind': 'N', 'filter': no_idx_path, 'rhs_idx': i, 'rhs': p_rlist[i]}
                if p_complex_details:
                    diff['rhs_idx'] = i
                    diff['rhs'] = p_rlist[i]
                current_diffs.append(diff)

    return current_diffs


def _get_list_diff_by_position(p_llist, p_rlist, p_path="", p_mapping=[], p_ignored_fields=[], p_simple_details=True, p_complex_details=False):
    """
        Compare two lists by position only, no matter they would have a matching id

        p_llist             The Left list to compare
        p_rlist             The right list to compare
        p_path              Path associated to the difference (useful for nested objects comparison)
        p_mapping           A mapping list of dict that associates a json path to a fiel containing the object id {'path':'path.to.object','id':'fieldname'}
        p_ignored_fields    List of path that will not be compared
        p_simple_details    If true, retrieves the values of "simple types differences" (int, float, string)
                            It will give the value for each version (old or new) of a field that is of simple type (int, string)
        p_complex_details   If true, retrieves the values of "complex types differences" (list, dict)

        return   A list of differences
    """
    current_diffs = []
    no_idx_path = _get_path_without_indexes(p_path)

    # Loop over the first list
    for i in range(len(p_llist)):
        # Record the deleted items (in llist but not in rlist)
        if (i >= len(p_rlist)):
            diff = {'path_to_object': p_path, 'kind': 'D', 'filter': no_idx_path}
            if p_complex_details:
                diff['lhs_idx'] = i
                diff['lhs'] = p_llist[i]
            current_diffs.append(diff)
        else:
            # If index exists in both lists, compute the diff between the two items
            diffs = get_diff(p_llist[i], p_rlist[i], p_path, p_mapping, p_ignored_fields, p_simple_details, p_complex_details)
            current_diffs.extend(diffs)

    # If there are more items in the rlist, loop over it to get new items
    if len(p_llist) < len(p_rlist):
        # New items (in rlist but not in llist)
        for i in range(len(p_llist), len(p_rlist)):
            diff = {'path_to_object': p_path, 'kind': 'N', 'filter': no_idx_path}
            if p_complex_details:
                diff['rhs_idx'] = i
                diff['rhs'] = p_rlist[i]
            current_diffs.append(diff)

    return current_diffs


def _add_field_to_path(p_path, p_field):
    """
        Add a field at the end of the path, with a "dot" separator

        p_path      The path to complete
        p_field     The field to add

        return a concatenation of p_path with p_field using a dot separator
    """
    if p_path:
        computed_path = "{0}.{1}".format(p_path, p_field)
    else:
        computed_path = p_field
    return computed_path


def _get_path_without_indexes(p_path):
    """
        We use two different format of the "json path" :
        - One is used to describe the difference. It contains list indexes for being able to recompute the full path to the object
        - One is more abstract : it is used in the conf to set the ids of nested object,
        or to set the field not to compare. This one doesn't contain any list index
        This function transforms a path describing a difference to an abstract one
    """
    # regexp = re.compile('\[[0-9]+\]')
    # no_idx_path = [field for field in p_path if not regexp.search(field)]

    # Replace expressions starting with a dot and between brackets
    no_idx_path = ""
    if p_path:
        no_idx_path = re.sub(r"\[[0-9]+\]\.", "", p_path)

    return no_idx_path


def _get_id_from_mapping(p_mapping, p_path):
    """
        Return the field name associated to a path in the mapping list or None if no field has been set
        to this path

        p_mapping   A mapping list as [{'path':'path.to.id', 'id':'thefieldname'},{'path':'an.other.path.to.id.anewfieldname','id':'anotherfieldname'}]
        p_path      A path to a nested objetc : 'path.to.a.nested.object'
    """

    # Search a matching path
    id_fieldname = next((item['id'] for item in p_mapping if item['path'] == p_path), None)
    return id_fieldname
