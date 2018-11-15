import json
from constants import Fields as F
from constants import NodeTypes as NT



# Assuming sql contains no more than one LIMIT

def correspond(node):
    highlight_vals = []
    node_type = node.attributes[F.NODE_TYPE]
    if node_type in NT.SCAN_TYPES:
        highlight_vals.append(node.attributes[F.RELATION_NAME])

    elif node_type == NT.CTE_SCAN:
        alias = node.attributes[F.CTE_NAME]
        highlight_vals.append('WITH %s'% alias)

    elif node_type == NT.HASH_JOIN:
        condition = remove_redundant_bracket(node.attributes[F.HASH_CONDITION])
        condition_reverse = reverse_condition(condition)
        highlight_vals.extend([condition, condition_reverse])

    elif node_type == NT.MERGE_JOIN:
        condition = remove_redundant_bracket(node.attributes[F.MERGE_CONDITION])
        condition_reverse = reverse_condition(condition)
        highlight_vals.extend([condition, condition_reverse])

    elif node_type == NT.NESTED_LOOP:
        highlight_vals.append(node.attributes[F.NLJ_CONDITION])

    elif node_type in NT.AGGREGATE_TYPES:
        highlight_vals.append("GROUP BY " + ', '.join(node.attributes[F.GROUP_KEY]))

    elif node_type == NT.SORT:
        sort_keys = []
        for k in node.attributes[F.SORT_KEY]:
            k = remove_redundant_bracket(k)
            sort_keys.append(k)
        highlight_vals.append("ORDER BY " + ', '.join(sort_keys))
        # highlight_vals.extend(node.attributes[F.SORT_KEY])


    elif node_type == NT.LIMIT:
        highlight_vals.append("LIMIT")

    else:
        highlight_vals = None
    return highlight_vals

def remove_redundant_bracket(str_val):
    if str_val.startswith('('):
        return remove_redundant_bracket(str_val[1:-1])
    return str_val


# A = B ==> B = A
def reverse_condition(condition):
    A, B = condition.split('=')
    res = ' = '.join([B, A]).strip()
    return res
