import json
from plan_processor import process_plan
from view import *
from visualizer import Visualizer

if __name__ == '__main__':
    query = open('sample_query.txt', 'r').read()
    qep = json.load(open("sample.json", "r"))
    process_plan(qep)
    # with open('out.json', 'w') as outfile:
    # 	json.dump(qep, outfile, indent=4)
    # viz = View(query, qep)
    # viz.show()

    visualizer = Visualizer()
    visualizer.start()
