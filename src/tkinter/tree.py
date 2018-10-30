from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Tree")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


tree = ttk.Treeview(mainframe)
# Inserted at the root, program chooses id:
tree.insert('', 'end', 'widgets', text='Widget Tour')
 
# Same thing, but inserted as first child:
tree.insert('', 0, 'gallery', text='Applications')

# Treeview chooses the id:
id = tree.insert('', 'end', text='Tutorial')

# Inserted underneath an existing node:
tree.insert('widgets', 'end', text='Canvas')
tree.insert(id, 'end', text='Tree')

tree.move('widgets', 'gallery', 'end')  # move widgets under gallery

tree.item('widgets', open=TRUE)
isopen = tree.item('widgets', 'open')

# tree = ttk.Treeview(root, columns=('size', 'modified'))
# tree['columns'] = ('size', 'modified', 'owner')

# tree.column('size', width=100, anchor='center')
# tree.heading('size', text='Size')

tree.grid()

# tree.set('widgets', 'size', '12KB')
# size = tree.set('widgets', 'size')
# tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))

# tree.insert('', 'end', text='button', tags=('ttk', 'simple'))
# tree.tag_configure('ttk', background='yellow')
# tree.tag_bind('ttk', '<1>', itemClicked)  # the item clicked can be found via tree.focus()

root.mainloop()