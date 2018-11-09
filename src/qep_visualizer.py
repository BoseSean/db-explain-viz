from constants import Fields as F
from constants import NaN
from tkinter import *
from tkinter import ttk
from json_parser import *
import uuid
from CustomText import CustomText
from highlighter import * 

class Visualizer(object):
	def __init__(self, query=None, plan=None, title='QEP Visualizer'):

		self.root = Tk()
		self.root.title(title)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)

		self.configure_layout(query, plan)

		self.hm = {}

		root = json_to_tree(plan)
		self.dfs(root)
		print(self.hm)
		self.mycolor = '#40E0D0' #(64, 204, 208)

		self.style = ttk.Style()
		# self.style.configure("highlight.TLabel", foreground="red", background="white")
		# self.style.configure("BW.TLabel", foreground="black", background="white")

	def configure_layout(self, query, plan):
		self.configure_qep_view(plan)
		self.configure_query_view(query)
		self.configure_master_view()
		self.configure_detail_view()
		self.configure_summary_view(plan)
		self.configure_button()

	def configure_qep_view(self, plan):
		self.qep_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.qep_view.grid(column=1, row=6, sticky=(N, W, E, S), rowspan=5)

		self.qep_text = Text(self.qep_view, height = 20, width = 70)
		self.qep_text.insert(END, json.dumps(plan, indent=1))
		self.qep_text.grid(column = 1, row = 1, sticky=(N, W, E, S))

	def configure_query_view(self, query):
		self.query_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.query_view.grid(column=1, row=1, sticky=(N, W, E, S), rowspan=5)

		self.query_text = CustomText(self.query_view, height = 20, width = 70)
		self.query_text.insert(END, query)
		self.query_text.tag_configure("highlight", background="yellow")
		self.query_text.grid(column = 1, row = 1, sticky=(S, W, E, N))


	def configure_master_view(self):
		self.master_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.master_view.grid(column=2, row=1, sticky=(N, W, E, S), rowspan=7)

		self.tree = ttk.Treeview(self.master_view, columns=('exe_time', 'percentage'))
		self.tree.column('exe_time', width=100, anchor='center')
		self.tree.heading('exe_time', text='exe_time / ms')

		self.tree.column('percentage', width=100, anchor='center')
		self.tree.heading('percentage', text='percentage')
		self.tree.pack(expand=True, fill='y')

		self.tree.bind("<Double 1>", self.itemClicked)

	def configure_detail_view(self):
		self.detail_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.detail_view.grid(column=3, row=1, sticky=(N, W, E, S), rowspan=11)
		ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
		ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))

	def configure_summary_view(self, plan):
		self.summary_view = ttk.Frame(self.root, padding="3 3 12 12")
		self.summary_view.grid(column=2, row=9, rowspan=3)
		self.show_summary_view(plan[0])

	def configure_button(self):
		self.explain_button = Button(self.root, text="Explain", width = 10, height = 5)
		self.explain_button.grid(column=1, row=11, sticky = (W, E))


	def show_summary_view(self, plan):
		r = 1
		for k,v in plan.items():
			if k == 'Plan':
				continue
			ttk.Label(self.summary_view, text=k,  style='BW.TLabel').grid(column=1, row=r, sticky=(W, S))
			ttk.Label(self.summary_view, text=v,  style='BW.TLabel').grid(column=2, row=r, sticky=(W, S))
			print(k, v)
			r += 1
			


	def get_summary(self, plan):
		return 'some text'

	def itemClicked(self, event):
		# node = self.hm[self.tree.selection()[0]]
		for t in self.hm.keys():
			self.tree.tag_configure(t, background='white')
		tag = self.tree.selection()[0]
		node = self.hm[tag]
		print(tag)
		self.tree.tag_configure(tag, background='yellow')
		self.detail(node)

		self.query_text.clear_highlight()
		highlight_vals = correspond(node)
		print('highlight', highlight_vals)
		if highlight_vals:
			for val in highlight_vals:
				self.query_text.highlight_pattern(val, "highlight")


	def itemHover(self, event, obj):
		# node = self.hm[self.tree.selection()[0]]
		node = self.hm[obj]
		self.detail(node)


	def add_node(self, node, parent_id=''):
		node_type = node.attributes['Node Type']
		t = str(id(node_type))
		# t = node.node_type
		self.tree.insert(parent_id, 0, t, text=node_type, tags=(t))
		self.tree.item(t, open=True)
		# self.tree.tag_configure(t, foreground='red')

		total_cost = node.attributes['Actual Total Time']
		startup_cost = node.attributes['Actual Total Time']
		self.tree.set(t, 'exe_time', str(total_cost - startup_cost))
		self.tree.set(t, 'percentage', '')
		self.hm[t]=node

		# self.tree.tag_bind(t, '<1>', lambda x, obj: self.itemHover)
		return t


	def detail(self, node):
		for child in self.detail_view.winfo_children():
			child.destroy()
		ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
		ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))
		r = 2
		for k,v in node.attributes.items():
			if k == 'Filter':
				print(v)
			ttk.Label(self.detail_view, text=k).grid(column=1, row=r, sticky=(W, S))
			ttk.Label(self.detail_view, text=v, style='highlight.TLabel').grid(column=2, row=r, sticky=(W, S))
			r += 1


	def show(self):
		self.root.mainloop()


	def dfs (self, node, parent_id=''):
		if not node:
			return
		id = self.add_node(node, parent_id)
		# print(node.attributes['Node Type'])
		if node.children:
			for child in node.children:
				self.dfs(child, id)


if __name__ == '__main__':	
	root = json_to_tree(None)
	viz = Visualizer()
	viz.dfs(root)
	for k,v in viz.hm.items():
		print(k, v.attributes['Node Type'])

	viz.show()

