#%%
from constants import Fields as F
from constants import NaN

def get(dic, key):
    # Get value from a dic, if key not exists, set as NaN
    if key not in dic:
        if key == F.PLANS:
            dic[key] = []
        else:
            dic[key] = NaN
    return dic[key]

def process_plan(explain_list):
    for e in explain_list:
        e[F.MAXIMUM_COSTS] = 0
        e[F.MAXIMUM_ROWS] = 0
        e[F.MAXIMUM_DURATION] = 0
        e[F.TOTAL_COST] = 0
        process(e[F.PLAN], e)

def process(plan, explain):
    # print(plan[F.NODE_TYPE])
    calculatePlannerEstimate(plan, explain)
    calculateActuals(plan, explain)
    calculateMaximums(plan, explain)

    for i in get(plan, F.PLANS):
        process(i, explain)
    return plan

def calculatePlannerEstimate(node, explain):
    node[F.PLANNER_ESTIMATE_FACTOR] = get(node, F.ACTUAL_ROWS) / get(node, F.PLAN_ROWS)
    # node[F.PLANNER_ESIMATE_DIRECTION] = EstimateDirection.under

    if get(node, F.PLANNER_ESTIMATE_FACTOR) < 1:
        # node[PLANNER_ESIMATE_DIRECTION] = EstimateDirection.over
        node[F.PLANNER_ESTIMATE_FACTOR] = get(node, F.PLAN_ROWS) / get(node, F.ACTUAL_ROWS)

def calculateActuals(node, explain):
        node[F.ACTUAL_DURATION] = get(node, F.ACTUAL_TOTAL_TIME)
        node[F.ACTUAL_COST] = get(node, F.TOTAL_COST)

        for subplan in get(node, F.PLANS):
            if get(subplan, F.NODE_TYPE) != F.CTE_SCAN:
               node[F.ACTUAL_DURATION] = get(node, F.ACTUAL_DURATION) - get(subplan, F.ACTUAL_TOTAL_TIME)
               node[F.ACTUAL_COST] = get(node, F.ACTUAL_COST) - get(subplan, F.TOTAL_COST)
            

        if get(node, F.ACTUAL_COST) < 0:
            node[F.ACTUAL_COST] = 0

        node[F.ACTUAL_DURATION] = get(node, F.ACTUAL_DURATION) * get(node, F.ACTUAL_LOOPS)
        ####**
        explain[F.TOTAL_COST] += get(node, F.ACTUAL_COST)

def calculateMaximums(node, explain):
    if explain[F.MAXIMUM_ROWS] < get(node, F.ACTUAL_ROWS):
        explain[F.MAXIMUM_ROWS] = get(node, F.ACTUAL_ROWS)

    if explain[F.MAXIMUM_COSTS] < get(node, F.ACTUAL_COST):
        explain[F.MAXIMUM_COSTS] = get(node, F.ACTUAL_COST)

    if explain[F.MAXIMUM_DURATION] < get(node, F.ACTUAL_DURATION):
        explain[F.MAXIMUM_DURATION] = get(node, F.ACTUAL_DURATION)
