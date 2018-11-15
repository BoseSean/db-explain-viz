from inspect import getmembers, isfunction

NaN = float("NaN")

class Fields:
    '''
    Fields contain all the possible attribute names of a node in QEP tree
    '''
    NODE_TYPE = 'Node Type'
    ACTUAL_ROWS = 'Actual Rows'
    PLAN_ROWS = 'Plan Rows'
    ACTUAL_TOTAL_TIME = 'Actual Total Time'
    ACTUAL_LOOPS = 'Actual Loops'
    TOTAL_COST = 'Total Cost'
    PLANS = 'Plans'
    PLAN = 'Plan'
    RELATION_NAME = 'Relation Name'
    SCHEMA = 'Schema'
    ALIAS = 'Alias'
    GROUP_KEY = 'Group Key'
    SORT_KEY = 'Sort Key'
    JOIN_TYPE = 'Join Type'
    INDEX_NAME = 'Index Name'
    INDEX_COND = 'Index Cond'
    HASH_CONDITION = 'Hash Cond'
    CTE_SCAN = "CTE Scan"
    CTE_NAME = "CTE Name"
    
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

class NodeTypes:
    '''
    All the node types (physical operators) of QEP tree
    '''
    SEQ_SCAN = 'Seq Scan'
    INDEX_SCAN = 'Index Scan'
    INDEX_ONLY_SCAN = 'Index Only Scan'
    BITMAP_HEAP_SCAN = 'Bitmap Heap Scan'
    BITMAP_INDEX_SCAN = 'Bitmap Index Scan'
    CTE_SCAN = 'CTE Scan'
    HASH_JOIN = 'Hash Join'
    MERGE_JOIN = 'Merge Join'
    NESTED_LOOP = 'Nested Loop'
    AGGREGATE = 'Aggregate'
    HASH_AGGREGATE = 'Hash Aggregate'
    SORT = 'Sort'
    LIMIT = 'Limit'

    SCAN_NORMAL_TYPES = [SEQ_SCAN, BITMAP_HEAP_SCAN]
    SCAN_INDEX_TYPES = [INDEX_SCAN, INDEX_ONLY_SCAN, BITMAP_INDEX_SCAN]
    SCAN_TYPES = SCAN_NORMAL_TYPES + SCAN_INDEX_TYPES
    AGGREGATE_TYPES = [AGGREGATE, HASH_AGGREGATE]

class Strings:
    TITLE = 'QEP Visualizer'
    HIGHLIGHT_LABEL = "highlight.TLabel"


if __name__=="__main__":
    for o in Fields.as_list():
        print(o)