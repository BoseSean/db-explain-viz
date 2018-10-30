from tkinter import *
from tkinter import ttk
from node import Node

class Visualizer(object):
	def __init__(self, title='QEP Visualizer'):
		self.root = Tk()
		self.root.title(title)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		self.master_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.master_view.grid(column=1, row=1, sticky=(N, W, E, S))

		self.detail_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.detail_view.grid(column=2, row=1, sticky=(N, W, E, S))

		self.tree = ttk.Treeview(self.master_view, columns=('exe_time', 'percentage'))
		self.tree.column('exe_time', width=100, anchor='center')
		self.tree.heading('exe_time', text='exe_time / ms')

		self.tree.column('percentage', width=100, anchor='center')
		self.tree.heading('percentage', text='percentage')
		self.tree.grid()
		self.hm = {}


	def itemClicked(self, event):
		print(self.hm)
		self.tree.focus()
		node = self.hm[self.tree.focus()]
		self.detail(node)

	# def add_node(self, node_id, text, parent_id='', pos='end'):
	# 	self.tree.insert(parent_id, pos, node_id, text=text)

	def add_node(self, node, parent_id=''):
		t = node.node_type
		self.tree.insert(parent_id, 0, t, text=t, tags=(t))

		self.tree.set(t, 'exe_time', str(node.total_cost - node.startup_cost))
		self.tree.set(t, 'percentage', '')
		self.hm[t]=node

		self.tree.tag_bind(t, '<1>', self.itemClicked)



	def detail(self, node):
		ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
		ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))
		r = 2
		for k,v in node.__dict__.items():
			ttk.Label(self.detail_view, text=k).grid(column=1, row=r, sticky=(W, S))
			ttk.Label(self.detail_view, text=v).grid(column=2, row=r, sticky=(W, S))
			r += 1


	


	def show(self):
		self.root.mainloop()

if __name__ == '__main__':	
	viz = Visualizer()
	limit = Node('LIMIT')
	limit.total_cost = 30
	limit.startup_cost = 30
	viz.add_node(limit)
	parent = Node('HASH')
	parent.total_cost = 30
	parent.startup_cost = 20
	viz.add_node(parent, 'LIMIT')
	# viz.detail(parent)
	viz.show()

