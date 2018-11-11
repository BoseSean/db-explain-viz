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
        query = open('../samples/sample_query.txt', 'r').read()
        plan = json.load(open("../samples/sample.json", "r"))
        self.view = View(self)
        self.on_new_plan(query, plan)


    def on_new_plan(self, query, plan):
        self.view.configure_layout(query, plan)
        self.tag_node_hm = {}
        process_plan(plan)
        root = json_to_tree(plan)
        self.dfs(root)
        print(self.tag_node_hm)

    def on_button_click(self):
        new_plan = json.loads(self.view.get_query_plan_text())
        new_query = self.view.get_query_text()
        self.on_new_plan(new_query, new_plan)

    def on_node_click(self, event):
        for t in self.tag_node_hm.keys():
            self.view.tree.tag_configure(t, background='white')
        tag = self.view.tree.selection()[0]
        node = self.tag_node_hm[tag]
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
        if node.children:
            for child in node.children:
                self.dfs(child, id)


    def start(self):
        self.view.show()
