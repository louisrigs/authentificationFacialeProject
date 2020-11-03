class _NodePriorityQueue:

	def __init__(self):
		self._heap = []

	def append(self, distance_index):
		hq.heappush(self._heap, distance_index)

	def pop(self):
		return hq.heappop(self._heap)

	def __len__(self):
		return len(self._heap)

class _KnnResultPriorityQueue:

	def __init__(self, max_size):
		self._max_size = max_size
		self._heap = []

	def push(self, index, distance):
		if len(self._heap) < self._max_size:
			hq.heappush(self._heap, (-distance, index))
		else:
			hq.heappushpop(self._heap, (-distance, index))

	def head_distance(self):
		return -self._heap[0][0]

	def get_all(self):
		return [r[1] for r in self._heap], [-r[0] for r in self._heap]

	def waiting_for_more(self):
		return len(self._heap) < self._max_size

class _KDNode:

	def __init__(self, data_idx):
		self._data_idx = data_idx
		self._split_axis = None
		self._split_value = None

	def search(self, query):
		side = None
		if self._split_axis != None:
			if query[self._split_axis] < self._split_value:
				side = 1
			else:
				side = 2
		return side

	def get_size(self):
		return len(self._data_idx)

	def is_leaf(self):
		return self._split_axis == None

	def get_split(self):
		split = None
		if self._split_axis != None:
			split = [self._split_axis, self._split_value]
		return split

class KDTree:
	""" Kd tree implementation

	Kd tree that supports three search algorithms:
	  * backtracking with maximum numbr of visited leaves;
	  * branch-and-bound;
	  * best bin first.

	The tree can accept an arbitrary number of elements in its leaves
	(specified at the construction of the object).
	The search uses the squared Euclidean distance.
	"""

	def __init__(self, leaf_size=1):
		""" Constructor for a KDTree object

		Constructor for a KDTree with leaf_size elements in its leaves.

		:param leaf_size: Maximum number of elements in a leaf.
		:rtype leaf_size: int
		"""
		self._leaf_size = leaf_size

	def build(self, data):
		""" Building a kd tree.

		Builds the KD tree from the data.

		:param data: data to index (numpy array of size n x d, with n
			the size of the dataset and d the dimension of the
			vectors).
		:type data: two-dimensional numpy array of floats
		"""
		self._data = data

		n, d = data.shape
		height = 2 + np.maximum(0, np.floor(np.log2((n-1) / self._leaf_size))).astype(np.int32)

		# Array of nodes
		self._nodes = np.empty((2**height-1,), dtype=np.object)


		self._nodes[0] = _KDNode(np.arange(n))
		for i in range(len(self._nodes)//2):
			if self._nodes[i] == None:
				continue
			# get node's data indices
			data_idx = self._nodes[i]._data_idx
			# split data
			if len(data_idx) > self._leaf_size:
				self._nodes[i]._split_axis, self._nodes[i]._split_value, left_idx, right_idx = self._split_data(data[data_idx])
				# get indices back to main data array basis
				left_idx = data_idx[left_idx]
				right_idx = data_idx[right_idx]
				# create children
				self._nodes[i*2+1] = _KDNode(left_idx)
				self._nodes[i*2+2] = _KDNode(right_idx)

	def _split_data(self, data):
		""" Splits the data along a dimension

		Splits the data along a dimension. The split dimension is the
		one with largest variance. The split value is the median along
		the split axis.

		:param data: the dataset to split
		:type data: two-dimensional Numpy array of floats

		:return: split axis, split value, left subarray (data indices,
			unsorted), right subarray(data indices, unsorted)
		:rtype: int, float, Numpy array of ints, Numpy array of ints
		"""
		data_variance = np.var(data, axis=0)
		split_axis = np.argmax(data_variance)
		ordered_idx = np.argpartition(data[:,split_axis], len(data)//2)
		split_value = (data[ordered_idx[len(data)//2], split_axis] + np.max(data[ordered_idx[:len(data)//2], split_axis])) / 2
		return split_axis, split_value, ordered_idx[:len(data)//2], ordered_idx[len(data)//2:]

	def search(self, query, k=1, max_visited_leaves=np.inf,
		 branch_and_bound=True, best_bin_first=True):
		""" Performs a search in the kd tree index

		Searches the nearest neighbors of a (single) query in the kd
		tree. Three search algorithms are available:
		  * backtracking (branch_and_bound==False and
			best_bin_first==False)
		  * branch-and-bound (branch_and_bound==True and
			best_bin_first==False)
		  * best bin first (branch_and_bound==True and
			best_bin_first==True)

		The naive search can be performed by setting
		max_visited_leaves=1.
		The distances to the query are computed using the squared
		euclidean distance.

		:param query: The query to search
		:param k: The number of NN to search
		:param max_visited_leaves: The maximum number of leaves to
			visit
		:param branch_and_bound: If True, branch-and-bound search is
			used
		:param best_bin_first: If True, best bin first search is used
		:type query: One-dimensional Numpy array of floats
		:type k: int
		:type max_visited_leaves: int
		:type branch_and_bound: boolean
		:type best_bin_first: boolean

		:return: number of processed samples, k NN (represented by
			their index in the original data matrix), distances of the
			returned NN to the query.
		:rtype: int, int list, float list
		"""
		processed_samples = 0
		current_node_idx = 0
		current_node = self._nodes[current_node_idx]
		if best_bin_first:
			nodes_to_visit = _NodePriorityQueue()
		else:
			nodes_to_visit = []
		search_results = _KnnResultPriorityQueue(k)

		# get first leaf matching the query
		while not current_node.is_leaf():
			next_node = current_node.search(query)
			other_node = 3 - next_node
			other_node_distance = np.abs(query[current_node._split_axis] - current_node._split_value)**2
			nodes_to_visit.append((other_node_distance, current_node_idx * 2 + other_node))
			current_node_idx = current_node_idx * 2 + next_node
			current_node = self._nodes[current_node_idx]

		# store results
		for x_idx in current_node._data_idx:
			search_results.push(x_idx, self._distance(self._data[x_idx], query))
		processed_samples += len(current_node._data_idx)

		# backtrack through the tree
		visited_leaves = 1
		while visited_leaves < max_visited_leaves and len(nodes_to_visit) > 0:
			current_node_distance, current_node_idx = nodes_to_visit.pop()
			if branch_and_bound and not search_results.waiting_for_more() \
					and current_node_distance >= search_results.head_distance():
				continue
			current_node = self._nodes[current_node_idx]
			if current_node.is_leaf():
				for x_idx in current_node._data_idx:
					search_results.push(x_idx, self._distance(self._data[x_idx], query))
				processed_samples += len(current_node._data_idx)
				visited_leaves += 1
			else:
				next_node = current_node.search(query)
				other_node = 3 - next_node
				other_node_distance = np.abs(query[current_node._split_axis] - current_node._split_value)**2
				nodes_to_visit.append((other_node_distance, current_node_idx * 2 + other_node))
				nodes_to_visit.append((0.0, current_node_idx * 2 + next_node))

		matches, distances = search_results.get_all()
		return processed_samples, matches, distances

	def _distance(self, data, query):
		""" Computes the squared Euclidean distance between two vectors.

		:param data: the data vector
		:param query: the query vector
		:type data: d-dimensional Numpy array of floats
		:type query: d-dimensional Numpy array of floats

		:return: Squared Euclidean distance between data and query
		:rtype: float
		"""
		return np.sum((data-query)**2)

	def get_splits(self):
		""" Gets the splits defined by the nodes of the kd tree

		Returns the splits contained in the nodes of the kd tree as a
		list containing:
		  * [split axis, split value] for internal nodes;
		  * None for leaf nodes.

		Nodes are in the order of a breadth-first search.

		:return: list containing the [split axis, split value] values
			for the internal nodes, None for leaf nodes.
		:rtype: list of [int, float] lists.
		"""
		return [n.get_split() for n in self._nodes]
