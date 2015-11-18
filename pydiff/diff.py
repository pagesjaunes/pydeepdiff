"""

    FIXME : LES DIFFERENCES A PARTIR DE LISTES NE MONTRENT PAS LE CHEMIN QUI INCLUE
    L'INDEX DE L'ELEMENT DANS LE TABLEAU


    Set of functions that handle differences between two objects
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

"""

import logging
import re

logger = logging.getLogger("diff")


def get_diff(p_lhs, p_rhs, p_path=[], p_mapping={}, p_ignored_fields=[]):
    """
        Computes difference between two objects
        p_lhs               Left Hand Side of the comparison
        p_rhs               Right Hand Side of the comparison
        p_path              Path associated to the difference (useful for nested objects comparison)
        p_mapping           A mapping dict that associates a json path to a fiel containing the object id
        p_ignored_fields    List of path that will not be compared
    """
    current_diffs = []  # Computed diffs

    # Check if the current path belongs to the paths list to ignore for comparison
    no_idx_path = _get_path_without_indexes(p_path)
    # import pdb; pdb.set_trace()
    if '.'.join(no_idx_path) in p_ignored_fields:
        return []

    if not isinstance(p_lhs, type(p_rhs)):
        # If the type are different, it corresponds to a creation and a deletion
        diff = {'path': p_path, 'kind': 'D', 'lhs': p_lhs}
        current_diffs.append(diff)
        diff = {'path': p_path, 'kind': 'N', 'rhs': p_rhs}
        current_diffs.append(diff)
    elif isinstance(p_lhs, dict):
        # Dictionary data
        current_diffs.extend(_get_dictionary_diff(p_lhs, p_rhs, p_path, p_mapping, p_ignored_fields))
    elif isinstance(p_lhs, list):
        # List data
        current_diffs.extend(_get_list_diff(p_lhs, p_rhs, p_path, p_mapping, p_ignored_fields))
    else:
        # Simple data
        current_diffs.extend(_get_simpletype_diff(p_lhs, p_rhs, p_path))

    return current_diffs


def _get_simpletype_diff(p_lst, p_rst, p_path=[]):
    """
        Generates a "E" diff if p_lst and p_rst are not equals

        p_lst       Left Simple Type
        p_rst       Right Simple Type
        p_path      The path of p_lst and p_rst if they "come" from a nested object

        return  A list of a single "diff" object if p_lst != p_rst, an empty one else
    """
    current_diffs = []

    if p_lst != p_rst:
        diff = {'path': p_path, 'kind': 'E', 'lhs': p_lst, 'rhs': p_rst}
        current_diffs.append(diff)

    return current_diffs


def _get_dictionary_diff(p_ldic, p_rdic, p_path=[], p_mapping={}, p_ignored_fields=[]):
    """
        Generates diff between two dictionaries.
        Creates "N" type diff for each key present only on the right side
        Creates "D" type diff for each key present only on the left side
        Creates as differences as they are in the nested objects

        p_ldic      Left Dictionary
        p_rdic      Right Dictionary
        p_path      Path associated to the difference (useful for nested objects comparison)
        p_mapping   A mapping dict that associates a json path to a field containing the object id
        p_ignored_fields    List of path that will not be compared

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
        current_path = p_path + [key]
        diff = {'path': current_path, 'kind': 'N', 'rhs': p_ldic[key]}
        current_diffs.append(diff)

    # Deletions
    for key in (p_rdic.keys() - intersect):
        # As the diff is on "key" field, we add it to the path
        current_path = p_path + [key]
        diff = {'path': current_path, 'kind': 'D', 'lhs': p_rdic[key]}
        current_diffs.append(diff)

    # Changes
    for key in intersect:
        # As the diff is on "key" field, we add it to the path
        current_path = p_path + [key]
        current_diffs.extend(get_diff(p_ldic.get(key), p_rdic.get(key), current_path, p_mapping, p_ignored_fields))

    return current_diffs


def _get_list_diff(p_llist, p_rlist, p_path=[], p_mapping={}, p_ignored_fields=[]):
    """
        Generates "A type" array diff

        p_llist         Left List
        p_rlist         Right List
        p_path          The path of p_llist and p_rlist if they "come" from a nested object
        p_mapping       A mapping dict that associates a json path to a fiel containing the object id
        p_ignored_fields    List of path that will not be compared

        return  A list of diff (type "A" as 'Array').
    """
    current_diffs = []

    # Detect the items list type
    item_type = None
    item_type = _get_list_type(p_llist)
    if not item_type:
        item_type = _get_list_type(p_rlist)

    if item_type == "dict":
        current_diffs = _get_list_dict_diff(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields)
    elif item_type == "list":
        current_diffs = _get_list_diff_by_position(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields)
    else:
        current_diffs = _get_list_simple_diff(p_llist, p_rlist, p_path)

    return current_diffs


def _get_list_type(p_list):
    """
        Returns the type of the list items
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


def _get_list_simple_diff(p_llist, p_rlist, p_path=[]):
    """
        Computes the diff between two lists containing simple type items

        p_llist         Left List containing simple type items
        p_rlist         Right List containing simple type items
        p_path          The path of p_llist and p_rlist if they "come" from a nested object

        return  A list of diff (type "A" as 'Array').
    """
    current_diffs = []

    # Deleted items
    left_not_in_right = [{'path': p_path, 'kind': 'D', 'lhs_idx': left_index, 'lhs': left_item} for left_index, left_item in enumerate(p_llist, start=0) if left_item not in p_rlist]

    # New items
    right_not_in_left = [{'path': p_path, 'kind': 'N', 'rhs_idx': right_index, 'rhs': right_item} for right_index, right_item in enumerate(p_rlist, start=0) if right_item not in p_llist]

    current_diffs.extend(left_not_in_right)
    current_diffs.extend(right_not_in_left)

    return current_diffs


def _get_list_dict_diff(p_llist, p_rlist, p_path=[], p_mapping={}, p_ignored_fields=[]):
    """
        Computes the diff between two lists containing dictionaries.
        Try to get a mapping from "p_mapping" to identify the fieldname that makes matchs possible
        If not fieldname can be gotten, a single "positionnal" diff is compute

        p_llist         Left dict List
        p_rlist         Right ditc List
        p_path          The path of p_llist and p_rlist if they "come" from a nested object
        p_mapping       A mapping dict that associates a json path to a field containing the object id
        p_ignored_fields    List of path that will not be compared

        return  A list of diff (type "A" as 'Array') + a list of true diff between subobject
    """
    current_diffs = []

    # Any id_field defined for this path ?
    try:
        # As the path stores indexes, we have to remove them to match the mapping format
        no_idx_path = _get_path_without_indexes(p_path)
        logger.debug("id_fieldname from %s", '.'.join(no_idx_path))
        id_fieldname = p_mapping['.'.join(no_idx_path)]
    except KeyError as e:
        # Can't compare elements by id, compare by position only
        logger.debug("No id_fieldname matching the path %s. Using positional comparaison for this list ...", '.'.join(no_idx_path))
        current_diffs = _get_list_diff_by_position(p_llist, p_rlist, p_path, p_mapping, p_ignored_fields)
    except Exception as e:
        logger.debug("error getting id_fieldname")
        logger.error(e)
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
                        diff = {'path': p_path, 'kind': 'M', 'lhs_idx': left_index, 'rhs_idx': right_index}
                        current_diffs.append(diff)

                    # We keep a trace of the list idx in the path
                    # Append the index of the element to the path
                    new_path = p_path.copy()
                    new_path.append("["+str(left_index)+"]")
                    current_diffs.extend(get_diff(left_item, right_item, new_path, p_mapping, p_ignored_fields))

                    # left_not_in_right and right_not_in_left store index
                    left_not_in_right.remove(left_index)
                    right_not_in_left.remove(right_index)
                else:
                    # Not "comparable" : each ones stay in the left_not_in_right and right_not_in_left lists for "D" and "N" diffs generation
                    logger.debug("Can't compare left and right : %s != %s", left_item.get(id_fieldname, None), right_item.get(id_fieldname, None))

        # Deleted items
        for i in left_not_in_right:
            diff = {'path': p_path, 'kind': 'D', 'lhs_idx': i, 'lhs':  p_llist[i]}
            current_diffs.append(diff)

        # New items
        for i in right_not_in_left:
            diff = {'path': p_path, 'kind': 'N', 'rhs_idx': i, 'rhs': p_rlist[i]}
            current_diffs.append(diff)

    return current_diffs


def _get_list_diff_by_position(p_llist, p_rlist, p_path=[], p_mapping={}, p_ignored_fields=[]):
    """
        Compares two lists by position only, no matter they would have a matching id
        p_llist     The Left list to compare
        p_rlist     The right list to compare
        p_path      Path associated to the difference (useful for nested objects comparison)
        p_mapping   A mapping dict that associates a json path to a fiel containing the object id
        p_ignored_fields    List of path that will not be compared

        return   A list of differences
    """
    current_diffs = []

    # Loop over the first list
    for i in range(len(p_llist)):
        # Record the deleted items (in llist but not in rlist)
        if (i >= len(p_rlist)):
            diff = {'path': p_path, 'kind': 'D', 'lhs_idx': i, 'lhs':  p_llist[i]}
            current_diffs.append(diff)
        else:
            # If index exists in both lists, compute the diff between the two items
            diffs = get_diff(p_llist[i], p_rlist[i], p_path, p_mapping, p_ignored_fields)
            current_diffs.extend(diffs)

    # If there are more items in the rlist, loop over it to get new items
    if len(p_llist) < len(p_rlist):
        # New items (in rlist but not in llist)
        for i in range(len(p_llist), len(p_rlist)):
            diff = {'path': p_path, 'kind': 'N', 'rhs_idx': i, 'rhs': p_rlist[i]}
            current_diffs.append(diff)

    return current_diffs


def _get_path_without_indexes(p_path):
    """
        We use two different format of the "json path" :
        - One is used to describe the difference. It contains list indexes for being able to recompute the full path to the object
        - One is more abstract : it is used in the conf to set the ids of nested object,
        or to set the field not to compare. This one doesn't contain any list index
        This function transforms a path describing a difference to an abstract one
    """
    regexp = re.compile('\[[0-9]+\]')
    no_idx_path = [field for field in p_path if not regexp.search(field)]

    return no_idx_path
