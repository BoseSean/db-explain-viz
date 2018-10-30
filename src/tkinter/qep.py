from tkinter import *
from tkinter import ttk

root = Tk()
root.title("QEP Visualizer")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


tree = ttk.Treeview(mainframe, columns=('exe_time', 'percentage'))
tree.column('exe_time', width=100, anchor='center')
tree.heading('exe_time', text='exe_time / ms')

tree.column('percentage', width=100, anchor='center')
tree.heading('percentage', text='percentage')
# Inserted at the root, program chooses id:
tree.insert('', 'end', 'limit', text='LIMIT')
tree.set('limit', 'exe_time', '< 1')
tree.set('limit', 'percentage', '0 %')

tree.insert('', 'end', 'sort', text='SORT')
tree.set('sort', 'exe_time', '1.36')
tree.set('sort', 'percentage', '0 %')

tree.insert('', 'end', 'hash1', text='HASH JOIN')
tree.set('hash1', 'exe_time', '125.19')
tree.set('hash1', 'percentage', '17 %')

tree.insert('hash1', 'end', 'hash2', text='HASH JOIN')
tree.set('hash2', 'exe_time', '36.78')
tree.set('hash2', 'percentage', '5 %')

tree.insert('hash1', 'end', 'hash3', text='HASH JOIN')
tree.set('hash3', 'exe_time', '20.97')
tree.set('hash3', 'percentage', '3 %')
 
# Same thing, but inserted as first child:
# tree.insert('', 0, 'gallery', text='Applications')
# tree.insert('', 0, 'sort', text='Applications')

# Treeview chooses the id:

# tree.move('limit', 'gallery', 'end')  # move limit under gallery

# tree.item('limit', open=TRUE)
# isopen = tree.item('limit', 'open')



tree.grid()

root.mainloop()