import json
from constants import Fields as F


# Assuming sql contains no more than one LIMIT

def correspond(node):
    highlight_vals = []
    node_type = node.attributes[F.NODE_TYPE]
    if node_type in ["Seq Scan", "Index Scan", "Index Only Scan"]:
        highlight_vals.append(node.attributes[F.RELATION_NAME])

    elif node_type == 'CTE Scan':
        alias = node.attributes[F.ALIAS]
        highlight_vals.append('WITH %s'% alias)

    elif node_type == "Hash Join":
        condition = remove_redundant_bracket(node.attributes[F.HASH_CONDITION])
        condition_reverse = reverse_condition(condition)
        highlight_vals.extend([condition, condition_reverse])

    elif node_type == "Merge Join":
        condition = remove_redundant_bracket(node.attributes[F.MERGE_CONDITION])
        condition_reverse = reverse_condition(condition)
        highlight_vals.extend([condition, condition_reverse])

    elif node_type == "Nested Loop":
        highlight_vals.append(node.attributes[F.NLJ_CONDITION])

    elif node_type in ["Aggregate", 'Hash Aggregate']:
        highlight_vals.append("GROUP BY " + ', '.join(node.attributes[F.GROUP_KEY]))

    elif node_type == "Sort":
        sort_keys = []
        for k in node.attributes[F.SORT_KEY]:
            k = remove_redundant_bracket(k)
            sort_keys.append(k)
        highlight_vals.append("ORDER BY " + ', '.join(sort_keys))
        # highlight_vals.extend(node.attributes[F.SORT_KEY])


    elif node_type == "Limit":
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
