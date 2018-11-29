from constants import Fields as F
from itertools import cycle
import json
import os
import sys

actual_values = set([F.ACTUAL_TOTAL_TIME, F.ACTUAL_STARTUP_TIME, F.ACTUAL_ROWS,F.ACTUAL_DURATION, F.ACTUAL_COST])

# =============== colored and formatted printing
class cprint:
    COLORS = cycle(['\033[41m', '\033[42m', '\033[43m'])
    ENDC = '\033[0m'

    def __init__(self, num):
        self.num = num
        self.set_color()
        self.out_buffs = [ [] for i in range(num) ]
    
    def set_color(self):
        self.HIGHLIGHT = next(self.COLORS)

    def p(self, num, indent_lev, if_highlight, s):
        if if_highlight:
            self.out_buffs[num].append(( s, indent_lev, self.HIGHLIGHT))
        else:
            self.out_buffs[num].append(( s, indent_lev, self.ENDC))

    def output(self, width):
        per_width = int((width-(self.num-1)*2) / self.num)
        for line in range(len(self.out_buffs[0])):
            line_all_buff = []
            for s_l in self.out_buffs:
                s_l = s_l[line]
                indent_by = s_l[1]
                color = s_l[2]
                w =  per_width - indent_by*2
                temp = [s_l[0][i:i+w] for i in range(0, len(s_l[0]), w)]
                temp = [" >"*indent_by+ color + i.ljust(w) +self.ENDC for i in temp]
                line_all_buff.append(temp)
            
            for real_line in list(map(list, zip(*line_all_buff))):
                print(" |".join(real_line))

# =============== Real algorithms
def get_human(dic, key):
    if key not in dic:
        return ''
    else:
        if isinstance(dic[key], (list,)):
            return ", ".join(map(str, dic[key]))
        return str(dic[key])

def diff(p1, p2, depth):
    # Travesail two QEP trees with recursion
    attrs = set(list(p1.keys()) + list(p2.keys()))
    for key in attrs:
        if key != F.PLANS:
            # condition for different attribute
            if key not in actual_values and ((key not in p1) or (key not in p2) or (p1[key] != p2[key])):
                printer.p(0, depth, True, key+": "+ get_human(p1, key))
                printer.p(1, depth, True, key+": "+ get_human(p2, key))
            else:
                printer.p(0, depth, False, key+": "+ get_human(p1, key))
                printer.p(1, depth, False, key+": "+ get_human(p2, key))
    printer.set_color() # change color for highlight 
    if F.PLANS in p1 and F.PLANS in p2:
        for subp1, subp2 in zip(p1[F.PLANS],p2[F.PLANS]):
            diff(subp1,subp2, depth+1)

# =============== Input and arguments processing
if len(sys.argv) == 3:
    plan1_path = sys.argv[1]
    plan2_path = sys.argv[2]
else:
    plan1_path = '../db/qep_1.json'
    plan2_path = '../db/qep_3.json'

plan1 = json.load(open(plan1_path, "r"))[0]['Plan']
plan2 = json.load(open(plan2_path, "r"))[0]['Plan']
(rows, columns) = os.popen('stty size', 'r').read().split()
printer = cprint(2)
diff(plan1,plan2, 0)
printer.output(int(columns))

if len(sys.argv) != 3:
    print("Usage: python3 qep_diff.py <qep1> <qep2>")
    print("Showing default sample...")

if os.name == 'nt':
    print("Using terminal that support ANSI escape sequences to see COLORS.")

print("Diffed "+ plan1_path+ " "+plan2_path)