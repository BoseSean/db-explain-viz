


def get(dic, key, default = None):

def process_plan(plan):
    calculatePlannerEstimate(plan)
    calculateActuals(plan)
    return plan

def calculatePlannerEstimate(node):
    node[PLANNER_ESTIMATE_FACTOR] = node.get(ACTUAL_ROWS) / node.get(PLAN_ROWS)
    node[PLANNER_ESIMATE_DIRECTION] = EstimateDirection.under

    if node[PLANNER_ESTIMATE_FACTOR] < 1:
        node[PLANNER_ESIMATE_DIRECTION] = EstimateDirection.over
        node[PLANNER_ESTIMATE_FACTOR] = node.get(PLAN_ROWS) / node.get(ACTUAL_ROWS)

def calculateActuals(node):
        node[ACTUAL_DURATION] = node.get(ACTUAL_TOTAL_TIME)
        node[ACTUAL_COST] = node.get(TOTAL_COST)

        console.log (node)
        _.each(node.Plans, subPlan => {
           console.log('processing chldren', subPlan)
           # since CTE scan duration is already included in its subnodes, it should be be
           # subtracted from the duration of this node
            if (subPlan[NODE_TYPE] !== CTE_SCAN) {
               node[ACTUAL_DURATION] = node[ACTUAL_DURATION] - subPlan[ACTUAL_TOTAL_TIME]
               node[ACTUAL_COST] = node[ACTUAL_COST] - subPlan[TOTAL_COST]
            }
        })

        if (node[ACTUAL_COST] < 0) {
            node[ACTUAL_COST] = 0
        }

        # since time is reported for an invidual loop, actual duration must be adjusted by number of loops
        node[ACTUAL_DURATION] = node[ACTUAL_DURATION] * node[ACTUAL_LOOPS]

if __name_- == '__main__':
    pass
    print("123")