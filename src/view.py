from tkinter import ttk
from tkinter import *
from custom_text import CustomText
from highlighter import *
from json_parser import *


class View(object):
    def __init__(self, event_handler, query=None, plan=None):
        self.handler = event_handler
        self.root = Tk()
        self.root.title('QEP Visualizer')
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.rowconfigure(0, weight=5)
        self.root.rowconfigure(0, weight=5)
        self.root.rowconfigure(0, weight=1)
        self.configure_layout(query, plan)
        self.configure_style()

    def configure_style(self):
        self.mycolor = '#40E0D0'  # (64, 204, 208)
        self.style = ttk.Style()
        self.style.configure("highlight.TLabel", foreground="red", background="white")
        self.style.configure("BW.TLabel", foreground="black", background="white")

    def configure_layout(self, query=None, plan=None):
        self.configure_qep_view(json.dumps(plan, indent=1))
        self.configure_query_view(query)
        self.configure_master_view()
        self.configure_detail_view()
        self.configure_summary_view(plan)
        self.configure_button()

    def configure_qep_view(self, plan):
        self.qep_view = ttk.Frame(self.root, padding="3 3 12 12")
        self.qep_view.grid(column=1, row=6, sticky=(N, W, E, S), rowspan=5)

        self.qep_text = Text(self.qep_view, height=20, width=70)
        if plan is not None:
            print('has plan')
            self.qep_text.insert(END, plan)
        self.qep_text.grid(column=1, row=1, sticky=(N, W, E, S))

    def configure_query_view(self, query):
        self.query_view = ttk.Frame(self.root, padding="3 3 12 12")
        self.query_view.grid(column=1, row=1, sticky=(N, W, E, S), rowspan=5)

        self.query_text = CustomText(self.query_view, height=20, width=70)
        if query:
            self.query_text.insert(END, query)
        self.query_text.tag_configure("highlight", background="yellow")
        self.query_text.grid(column=1, row=1, sticky=(S, W, E, N))

    def configure_master_view(self):
        self.master_view = ttk.Frame(self.root, padding="3 3 12 12")
        self.master_view.grid(column=2, row=1, sticky=(N, W, E, S), rowspan=7)

        self.tree = ttk.Treeview(self.master_view, columns=('exe_time', 'percentage'))
        self.tree.column('exe_time', width=100, anchor='center')
        self.tree.heading('exe_time', text='exe_time / ms')

        self.tree.column('percentage', width=100, anchor='center')
        self.tree.heading('percentage', text='percentage')
        self.tree.pack(expand=True, fill='y')

        self.tree.bind("<Double 1>", self.handler.on_node_click)

    def configure_detail_view(self):
        self.detail_view = ttk.Frame(self.root, padding="3 3 12 12")
        self.detail_view.grid(column=3, row=1, sticky=(N, W, E, S), rowspan=11)
        ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
        ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))

    def configure_summary_view(self, plan):
        # self.summary_view = ttk.Frame(self.root)
        self.summary_view = Frame(self.root, bg='white', padx=3, pady=12)
        self.summary_view.grid(column=2, row=8, rowspan=2)
        # self.summary_view.pack(expand=True, fill='y')
        if plan:
            self.show_summary_view(plan[0])

    def configure_button(self):
        self.explain_button = Button(self.root, text="Explain", width=10, height=5, command=self.handler.on_button_click)
        self.explain_button.grid(column=1, row=11, sticky=(W, E))

    def show_summary_view(self, plan):
        r = 0
        for k, v in plan.items():
            if k == 'Plan':
                continue
            Label(self.summary_view, text=k, bg="white").grid(column=1, row=r, sticky=(W, S))
            Label(self.summary_view, text=v, bg="white").grid(column=2, row=r, sticky=(W, S))
            r += 1

    def add_node(self, node, parent_id=''):
        node_type = node.attributes['Node Type']
        t = str(id(node_type))
        self.tree.insert(parent_id, 0, t, text=node_type, tags=(t))
        self.tree.item(t, open=True)

        total_cost = node.attributes['Actual Total Time']
        startup_cost = node.attributes['Actual Total Time']
        self.tree.set(t, 'exe_time', str(total_cost - startup_cost))
        self.tree.set(t, 'percentage', '')
        self.handler.tag_node_hm[t] = node

        return t

    def detail(self, node):
        for child in self.detail_view.winfo_children():
            child.destroy()
        ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
        ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))
        r = 2
        for k, v in node.attributes.items():
            if k == 'Filter':
                print(v)
            ttk.Label(self.detail_view, text=k).grid(column=1, row=r, sticky=(W, S))
            ttk.Label(self.detail_view, text=v, style='BW.TLabel').grid(column=2, row=r, sticky=(W, S))
            r += 1

    def show(self):
        self.root.mainloop()

    def get_query_plan_text(self):
        return self.qep_text.get("1.0",END)

    def set_query_plan_text(self, query_plan):
        self.qep_text.insert(END, query_plan)

    def get_query_text(self):
        return self.query_text.get('1.0', END)

    def set_query_text(self):
        self.query_text.insert(END, query)


if __name__ == '__main__':
    root = json_to_tree(None)
    viz = View()
    viz.dfs(root)
    for k, v in viz.hm.items():
        print(k, v.attributes['Node Type'])

    viz.show()
