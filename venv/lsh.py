import numpy as np
import brute_force_search as bfs
import heapq as hq
import time as tm

class _LSHEntry:

	def __init__(self, data_id, signature):
		self._data_id = data_id
		self._signature = signature

	def __eq__(self, other):
		return self._signature == other._signature

class LSH:
	"""LSH index with regular search and multi-probe search.

	Implementation of E2LSH (LSH for Euclidean-norm). The index contains
	nb_tables hash tables, each using a hash function based on
	nb_projections random projections and a quantization step W.

	:param nb_projections: Number of projections in the hash function of
		 each table.
	:param nb_tables: Number of hash tables.
	:param w: Quantization step of the hash functions.
	:param seed: Seed of the random generator for reproducible experiments.
	:type nb_projections: int
	:type nb_tables: int
	:type w: int
	:type seed: int
	"""

	def __init__(self, nb_projections, nb_tables, w, seed=0):
		self._nb_projections = nb_projections
		self._nb_tables = nb_tables
		self._w = w
		# magic prime for effective hashing
		# (cf. Andoni/Indyk's implementation)
		self._HASH_PRIME = (2 << 31) - 5
		self._TABLE_LENGTH = 2 << 16
		np.random.seed(seed)

	def _generate_vector_projections(self, dimension):
		self._vector_projections = np.random.normal(0, 1, (self._nb_tables, self._nb_projections, dimension))
		self._vector_projections = (self._vector_projections.T / np.linalg.norm(self._vector_projections, axis = 2).T).T
		self._bias = np.random.uniform(0, self._w, (self._nb_tables, self._nb_projections))

	def _generate_signature_projections(self):
		self._signature_projections = np.random.uniform(0, np.random.uniform(0, 2 << 32), (self._nb_projections,)).astype(np.int32)

	def _hash_vector(self, x):
		return ((np.dot(self._vector_projections, x) + self._bias) / self._w).astype(np.int32)

	def _hash_vector_signatures(self, q):
		return np.abs((np.dot(q, self._signature_projections).astype(np.int64)%self._HASH_PRIME)%self._TABLE_LENGTH)

	def _build_tables(self):
		self._tables = np.empty((self._nb_tables, self._TABLE_LENGTH), dtype=np.object)
		for i in range(self._nb_tables):
			for j in range(self._TABLE_LENGTH):
				self._tables[i,j] = []

	def build(self, data):
		"""Builds the LSH index from the data

		:param data: The data as a (n,d)-shaped Numpy array (n =
			dataset size, d = data dimension).
		:type data: (n,d)-shaped Numpy array.
		"""
		self._data = data
		n, d = data.shape

		# generate random stuff and build tables
		self._generate_vector_projections(d)
		self._generate_signature_projections()
		self._build_tables()

		# populate hash tables with data
		for i, d in enumerate(data):
			signatures = self._hash_vector(d)
			hashs = self._hash_vector_signatures(signatures)
			for t, bucket in enumerate(self._tables[np.arange(len(self._tables)), hashs]):
				bucket.append((i, signatures[t]))

	def search(self, query, k=1, multi_probe=0):
		""" Search for the k-NN of query q in the index.

		:param query: the query (or probe) to search.
		:param k: the number of nearest neighbors to return
		:param multi_probe: the number of perturbations to use for
			multi-probe querying (if 0, multi-probe querying is
			desactivated.
		:type query: (d,)-shaped Numpy array
		:type k: int
		:type multi_probe: int

		:return: (nb_matches, matches, distances) with nb_matches the
			size of the short-list on which brute-force search is
			performed, matches the indices of the k-NN in the
			data matrix, and distances the values of the distances
			of the matches to the query.
		:rtype: (int, int list, float list)
		"""
		t1 = tm.time()
		signatures = self._hash_vector(query)
		hashs = self._hash_vector_signatures(signatures)

		# Get matches from buckets
		matches = set()
		t1 = tm.time()
		for signature, bucket in zip(signatures, self._tables[np.arange(len(self._tables)), hashs]):
			for e in bucket:
#				if (e[1] == signature).all():
				matches.add(e[0])

		# multiprobe search
		if multi_probe > 0:
			t1 = tm.time()
			for t in range(self._nb_tables):
				mp_signatures = self._generate_query_specific_perturbations(query, signatures[t], t, multi_probe) + signatures[t]
				mp_hashs = self._hash_vector_signatures(mp_signatures)
				for bucket, mp_signature in zip(self._tables[t,mp_hashs], mp_signatures):
					for e in bucket:
#						if (e[1] == mp_signature).all():
						matches.add(e[0])

		# brute-force search over matches
		matches = np.array(list(matches))
		if len(matches) > 0:
			t1 = tm.time()
			m, distances = bfs.knn_search(self._data[matches], query, k=k, norm="L2")
		else:
			m = []
			distances = []
		return len(matches), matches[m], distances

	def _generate_query_specific_perturbations(self, query, query_signature, table_idx, nb_perturbations):
		# get perturbation scores
		perturbation_scores = np.zeros(self._nb_projections * 2, dtype=np.float32)
		perturbation_scores[:self._nb_projections] = (np.dot(self._vector_projections[table_idx], query) + self._bias[table_idx]) - (query_signature * self._w)
		perturbation_scores[self._nb_projections:] = self._w - perturbation_scores[:self._nb_projections]

		# sort them
		sorted_perturbations = np.argsort(perturbation_scores)

		# now iterate over possible perturbation sets
		scores_candidates = [(perturbation_scores[sorted_perturbations[0]]**2, [0])]
		valid_candidates = []
		for i in range(nb_perturbations):
			valid = False
			while not valid:
				current_score, current_candidate = hq.heappop(scores_candidates)
				shift_candidate = list(current_candidate)
				shift_candidate[-1] = shift_candidate[-1] + 1
				shift_score = current_score - perturbation_scores[sorted_perturbations[current_candidate[-1]]]**2 \
						+ perturbation_scores[sorted_perturbations[shift_candidate[-1]]]**2
				expand_candidate = list(current_candidate)
				expand_candidate.append(current_candidate[-1]+1)
				expand_score = current_score + perturbation_scores[sorted_perturbations[expand_candidate[-1]]]**2
				hq.heappush(scores_candidates, (shift_score, shift_candidate))
				hq.heappush(scores_candidates, (expand_score, expand_candidate))
				valid = self._is_mp_candidate_valid(current_candidate)
			valid_candidates.append(current_candidate)

		final_perturbations = np.zeros((nb_perturbations, self._nb_projections))
		for i, c in enumerate(valid_candidates):
			c = sorted_perturbations[c]
			final_perturbations[i,c[c < self._nb_projections]] = -1
			final_perturbations[i,c[c >= self._nb_projections]-self._nb_projections] = 1
		return final_perturbations

	def _is_mp_candidate_valid(self, candidate):
		for i in range(len(candidate)):
			if i >= 2 * self._nb_projections or (2 * self._nb_projections - i - 1) in candidate:
				return False
		return True
