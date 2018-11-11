from view import View
from plan_processor import process_plan
import json
from json_parser import *
from highlighter import *

class EventHandler():
    def on_button_click(self):
        pass

    def on_node_click(self):
        pass

class Visualizer(EventHandler):
    def __init__(self):
        self.hm = {}
        query = open('sample_query.txt', 'r').read()
        qep = json.load(open("sample.json", "r"))
        process_plan(qep)
        self.view = View(self, query, qep)
        # root = json_to_tree(qep)
        # self.dfs(root)
        self.process(qep)

    def on_button_click(self):
        new_plan = json.loads(self.view.get_query_plan_text())
        new_query = self.view.get_query_text()
        self.view.configure_layout(new_query, new_plan)
        self.hm = {}
        root = json_to_tree(new_plan)
        self.dfs(root)

    def on_node_click(self, event):
        for t in self.hm.keys():
            self.view.tree.tag_configure(t, background='white')
        tag = self.view.tree.selection()[0]
        node = self.hm[tag]
        print(tag)
        self.view.tree.tag_configure(tag, background='yellow')
        self.view.detail(node)

        self.view.query_text.clear_highlight()
        highlight_vals = correspond(node)
        print('highlight', highlight_vals)
        if highlight_vals:
            for val in highlight_vals:
                self.view.query_text.highlight_pattern(val, "highlight")

    def dfs(self, node, parent_id=''):
        if not node:
            return
        id = self.view.add_node(node, parent_id)
        # print(node.attributes['Node Type'])
        if node.children:
            for child in node.children:
                self.dfs(child, id)

    def process(self, plan):
        self.hm = {}
        root = json_to_tree(plan)
        self.dfs(root)
        print(self.hm)

    def start(self):
        self.view.show()
