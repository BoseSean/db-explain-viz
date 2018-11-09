from inspect import getmembers, isfunction

NaN = float("NaN")

class Fields:
    NODE_TYPE = 'Node Type'
    ACTUAL_ROWS = 'Actual Rows'
    PLAN_ROWS = 'Plan Rows'
    ACTUAL_TOTAL_TIME = 'Actual Total Time'
    ACTUAL_LOOPS = 'Actual Loops'
    TOTAL_COST = 'Total Cost'
    PLANS = 'Plans'
    RELATION_NAME = 'Relation Name'
    SCHEMA = 'Schema'
    ALIAS = 'Alias'
    GROUP_KEY = 'Group Key'
    SORT_KEY = 'Sort Key'
    JOIN_TYPE = 'Join Type'
    INDEX_NAME = 'Index Name'
    HASH_CONDITION = 'Hash Cond'
    CTE_SCAN = "CTE Scan"
    
    COMPUTED_TAGS = '*Tags'
    COSTLIEST_NODE = '*Costiest Node (by cost)'
    LARGEST_NODE = '*Largest Node (by rows)'
    SLOWEST_NODE = '*Slowest Node (by duration)'

    MAXIMUM_COSTS = '*Most Expensive Node (cost)'
    MAXIMUM_ROWS = '*Largest Node (rows)'
    MAXIMUM_DURATION = '*Slowest Node (time)'
    ACTUAL_DURATION = '*Actual Duration'
    ACTUAL_COST = '*Actual Cost'
    PLANNER_ESTIMATE_FACTOR = '*Planner Row Estimate Factor'
    PLANNER_ESIMATE_DIRECTION = '*Planner Row Estimate Direction'

    @staticmethod
    def as_list():
        return list( 
            map(lambda i: i[1],
                filter(lambda i: i[0][0]!='_', 
                    getmembers(Fields, lambda x: not isfunction(x))
                )
            )
        )

if __name__=="__main__":
    for o in Fields.as_list():
        print(o)