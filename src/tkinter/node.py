class Node(object):
	def __init__(self, node_type):
		self.node_type = node_type
		self.startup_cost = None
		self.total_cost = None
		self.plan_rows = None
		self.plan_width = None
		self.acutal_startup_time = None
		self.actual_total_time = None
		self.actual_rows = None
		self.actual_loops = None
		self.output = None
		self.shared_hit_blocks = None
		self.shared_written_blocks = None
		self.local_hit_blocks = None

		# TODO: not complete