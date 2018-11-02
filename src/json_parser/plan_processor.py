from constants import Fields as F
from constants import NaN

def get(dic, key):
    # Get value from a dic, if key not exists, set as NaN
    if key not in dic:
        dic[key] = NaN
    return dic[key]

def process_plan(plan, explain):
    calculatePlannerEstimate(plan, explain)
    calculateActuals(plan, explain)
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

        print(node)
        for subplan in node[F.Plans]:
            if get(subplan, F.NODE_TYPE) !== F.CTE_SCAN:
               node[F.ACTUAL_DURATION] = get(node, F.ACTUAL_DURATION) - get(subplan, F.ACTUAL_TOTAL_TIME)
               node[F.ACTUAL_COST] = get(node, F.ACTUAL_COST) - get(subplan, F.TOTAL_COST)
            

        if get(node, F.ACTUAL_COST < 0:
            node[F.ACTUAL_COST] = 0

        node[F.ACTUAL_DURATION] = get(node, F.ACTUAL_DURATION) * get(node, F.ACTUAL_LOOPS)
        explain[F.TOTAL_COST] += get(node, F.ACTUAL_COST)


if __name_- == '__main__':
    pass