import json
from constants import Fields as F

class Node(object):
    '''
    A node in QEP tree presents a physical operator
    '''
    def __init__(self, attributes):
        self.attributes = attributes
        if F.PLANS in attributes:
            # del self.attributes['Plans']
            self.children = self.get_children_nodes(attributes[F.PLANS])
            del self.attributes[F.PLANS]
        else:
            self.children = None

    def get_children_nodes(self, children_list):
        children_nodes = []
        for child in children_list:
            node = Node(child)
            children_nodes.append(node)
        return children_nodes


def json_to_tree(json_str=None):
    '''
    Parse a json string to a tree containing Nodes object
    :param json_str:
    :return: the root node of QEP tree
    '''
    if not json_str:
        sample = open('sample.json').read()
        data = json.loads(sample)
        root = Node(data[0][F.PLAN])
        return root
    root = Node(json_str[0][F.PLAN])
    return root
