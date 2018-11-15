from tkinter import ttk
from tkinter import *
from highlighter import *
from json_parser import *
from constants import Fields as F
from constants import Strings as St


class View(object):
    def __init__(self, event_handler):
        self.handler = event_handler
        self.root = Tk()
        self.root.title(St.TITLE)
        self.configure_layout()
        self.configure_style()


    def configure_style(self):
        self.style = ttk.Style()
        self.style.configure(St.HIGHLIGHT_LABEL, foreground="red", background="white")
        self.style.configure("BW.TLabel", foreground="black", background="white")

    def configure_layout(self):

        self.configure_qep_view()
        self.configure_query_view()
        self.configure_master_view()
        self.configure_detail_view()
        self.configure_summary_view()
        self.configure_button()


    def configure_qep_view(self):
        self.qep_view = ttk.Frame(self.root, padding="3 3 12 12")
        self.qep_view.grid(column=1, row=6, sticky=(N, W, E, S), rowspan=5)

        self.qep_text = Text(self.qep_view, height=20, width=70)

        self.qep_text.grid(column=1, row=1, sticky=(N, W, E, S))

    def configure_query_view(self):
        self.query_view = ttk.Frame(self.root, padding="3 3 12 12")
        self.query_view.grid(column=1, row=1, sticky=(N, W, E, S), rowspan=5)

        self.query_text = CustomText(self.query_view, height=20, width=70)
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
        # self.detail_view = Frame(self.root, width='200')
        self.detail_view.grid(column=3, row=1, sticky=(N, W, E, S), rowspan=11)
        ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
        ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))

    def configure_summary_view(self):
        self.summary_view = Frame(self.root, bg='white', padx=3, pady=12)
        # self.summary_view = ttk.Frame(self.root)
        self.summary_view.grid(column=2, row=8, rowspan=2)

    def configure_button(self):
        self.explain_button = Button(self.root, text="Explain", width=10, height=5, command=self.handler.on_button_click)
        self.explain_button.grid(column=1, row=11, sticky=(W, E))

    def show_summary_view(self, plan):
        for child in self.summary_view.winfo_children():
            print(child)
            child.destroy()
        r = 0
        for k, v in plan.items():
            if k == 'Plan':
                continue
            if k == 'Execution Time':
                self.execution_time = float(v)
            Label(self.summary_view, text=k, bg="white").grid(column=1, row=r, sticky=(W, S))
            Label(self.summary_view, text=v, bg="white").grid(column=2, row=r, sticky=(W, S))
            # ttk.Label(self.summary_view, text=k).grid(column=1, row=r, sticky=(W, S))
            # ttk.Label(self.summary_view, text=v).grid(column=2, row=r, sticky=(W, S))
            r += 1

    def add_node(self, node, parent_id=''):
        node_type = node.attributes['Node Type']
        t = str(id(node_type))
        self.tree.insert(parent_id, 0, t, text=node_type, tags=(t))
        self.tree.item(t, open=True)

        duration = float(node.attributes[F.ACTUAL_DURATION])
        self.tree.set(t, 'exe_time', "%.2f"%(duration))
        self.tree.set(t, 'percentage', '%.2f'% (duration/self.execution_time))
        self.handler.tag_node_hm[t] = node

        return t

    def detail(self, node):
        for child in self.detail_view.winfo_children():
            child.destroy()
        ttk.Label(self.detail_view, text='ATTRIBUTE').grid(column=1, row=1, sticky=(W, S))
        ttk.Label(self.detail_view, text="VALUE").grid(column=2, row=1, sticky=(W, S))
        r = 2
        for k, v in node.attributes.items():
            if type(v) == type(0.0):
                v = "%.2f" % float(v)
            ttk.Label(self.detail_view, text=k).grid(column=1, row=r, sticky=(W, S))
            if type(v) == type([]):
                for i in range(len(v)):
                    ttk.Label(self.detail_view, text=v[i], style='BW.TLabel').grid(column=2, row=r, sticky=(W, S))
                    r+= 1
            else:
                ttk.Label(self.detail_view, text=v, style='BW.TLabel').grid(column=2, row=r, sticky=(W, S))
                r += 1

    def show(self):
        self.root.mainloop()

    def get_query_plan_text(self):
        return self.qep_text.get("1.0",END)

    def set_query_plan_text(self, query_plan):
        self.show_summary_view(query_plan[0])
        self.qep_text.delete('1.0', END)
        self.qep_text.insert(END, json.dumps(query_plan, indent=1))


    def get_query_text(self):
        return self.query_text.get('1.0', END)


    def set_query_text(self, query):
        self.query_text.delete('1.0', END)
        self.query_text.insert(END, query)


class CustomText(Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)
        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def clear_highlight(self):
        for tag in self.tag_names():
            self.tag_remove(tag, 1.0, END)

