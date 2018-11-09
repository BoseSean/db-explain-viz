import json
from plan_processor import process_plan
from qep_visualizer import *

if __name__ == '__main__':
	query = open('sample_query.txt', 'r').read()
	qep = json.load(open("simple_sample.json","r"))
	process_plan(qep)
	# with open('out.json', 'w') as outfile:
	# 	json.dump(qep, outfile, indent=4)
	viz = Visualizer(query, qep)
	viz.show()