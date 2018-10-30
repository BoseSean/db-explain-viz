import json

sample = open('sample.json').read()

sample_single = ''' [                             
   {                           
     "Plan": {                 
       "Node Type": "Seq Scan",
       "Relation Name": "foo", 
       "Alias": "foo",         
       "Startup Cost": 0.00,   
       "Total Cost": 155.00,   
       "Plan Rows": 10000,     
       "Plan Width": 4,         
     }                         
   }                           
 ]
'''
data = json.loads(sample)
def get_children_nodes(children_list):
	children_nodes = []
	for child in children_list:
		node = Node(child)
		children_nodes.append(node)
	return children_nodes

class Node(object):
	def __init__(self, attributes):
		self.attributes = attributes
		if 'Plans' in attributes:
			# del self.attributes['Plans']
			self.children = get_children_nodes(attributes['Plans'])
			del self.attributes['Plans']
		else:
			self.children = None

root = Node(data[0]['Plan'])

def dfs (node):
	if not node:
		return
	print(node.attributes['Node Type'])
	if node.children:
		for child in node.children:
			dfs(child)
dfs(root)
