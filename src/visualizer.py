from view import View
from plan_processor import process_plan
import json
from json_parser import *
from highlighter import *
import re

class Visualizer():
    '''
    Controller class
    '''
    def __init__(self):
        query = open('../samples/sample_query.txt', 'r').read()
        plan = json.load(open("../samples/sample.json", "r"))
        self.view = View(self)
        self.on_new_plan(query, plan)


    def on_new_plan(self, query, plan):
        '''
        When there is a new query and new QEP, the application will generate a tree view for QEP tree,
        and display summary statistics.
        :param query: SQL query
        :param plan: QEP in Json format
        :return: nothing
        '''
        self.view.configure_layout()
        process_plan(plan)
        self.view.set_query_plan_text(plan)
        self.view.set_query_text(query)
        self.tag_node_hm = {}
        root = json_to_tree(plan)
        self.dfs(root)

    def on_button_click(self):
        '''
        When the 'EXPLAIN' button is clicked, the application will get the text from query view and QEP view
        and process the new plan
        :return:
        '''
        new_plan = json.loads(self.view.get_query_plan_text())
        new_query = self.view.get_query_text()
        self.on_new_plan(new_query, new_plan)

    def on_node_click(self, event):
        '''
        When a node in the QEP tree is clicked, the details of the node is displayed in detail view.
        The correlated components in SQL query is also highlighted
        :param event:
        :return: nothing
        '''
        for t in self.tag_node_hm.keys():
            self.view.tree.tag_configure(t, background='white')
        tag = self.view.tree.selection()[0]
        node = self.tag_node_hm[tag]
        self.view.tree.tag_configure(tag, background='yellow')
        self.view.detail(node)

        self.view.query_text.clear_highlight()
        highlight_vals = find_correspond(node)

        if highlight_vals:
            for val in highlight_vals:
                val = val.replace('(', '\(').replace(')', '\)')
                print(val)
                self.view.query_text.highlight_pattern(val, "highlight", regexp=True)

    def dfs(self, node, parent_id=''):
        '''
        Use dfs to build QEP tree
        :param node: root node of QEP tree
        :param parent_id: node id of the parent
        :return: nothing
        '''
        if not node:
            return
        id = self.view.add_node(node, parent_id)
        if node.children:
            for child in node.children:
                self.dfs(child, id)


    def start(self):
        self.view.show()
