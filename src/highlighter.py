import json
from constants import Fields as F

#Assuming sql contains no more than one LIMIT

def correspond (node):
  highligh_vals = []
  node_type = node.attributes[F.NODE_TYPE]
  if node_type == "Seq Scan":
    highligh_vals.extend([node.attributes[F.RELATION_NAME]])

  elif node_type == "Hash Join":
    condition = remove_redundant_bracket(node.attributes[F.HASH_CONDITION])
    condition_reverse = reverse_condition(condition)
    highligh_vals.extend([condition, condition_reverse])

  elif node_type == "Aggregate":
    highligh_vals.extend(["GROUP BY " + ', '.join(node.attributes[F.GROUP_KEY])])
    # highligh_vals.extend(["Group by"])
    # highligh_vals.extend()

  elif node_type == "Sort":
    sort_keys = []
    for k in node.attributes[F.SORT_KEY]:
      if k.startswith('('):
        sort_keys.append(k[1:-1]) # remove the outter most bracket of keys
      else:
        sort_keys.append(k)
    highligh_vals.extend(["ORDER BY " + ', '.join(sort_keys)])
    # highligh_vals.extend(node.attributes[F.SORT_KEY])


  elif node_type == "Limit":
    highligh_vals.extend(["LIMIT"])

  else:
    highligh_vals = None
  return highligh_vals


def remove_redundant_bracket(str_val):
  if str_val.startswith('('):
    return remove_redundant_bracket(str_val[1:-1])
  return str_val


# A = B ==> B = A
def reverse_condition(condition):
  A, B = condition.split('=')
  res = ' = '.join([B, A]).strip()
  print(res)
  return res

