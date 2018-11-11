import json


class Node(object):
    def __init__(self, attributes):
        self.attributes = attributes
        if 'Plans' in attributes:
            # del self.attributes['Plans']
            self.children = self.get_children_nodes(attributes['Plans'])
            del self.attributes['Plans']
        else:
            self.children = None

    def get_children_nodes(self, children_list):
        children_nodes = []
        for child in children_list:
            node = Node(child)
            children_nodes.append(node)
        return children_nodes


def json_to_tree(json_str=None):
    if not json_str:
        sample = open('sample.json').read()
        data = json.loads(sample)
        root = Node(data[0]['Plan'])
        return root
    root = Node(json_str[0]['Plan'])
    return root
