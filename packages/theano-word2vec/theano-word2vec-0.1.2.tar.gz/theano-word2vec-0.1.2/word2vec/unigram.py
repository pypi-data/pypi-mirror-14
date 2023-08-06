'''
Calculates the maximum likelihood probability of single words, as equal
to their frequency within a corpus, and enables efficiently sampling
from the distribution.

Assumes that the words have been converted into ids that were assigned
by auto-incrementing from 0 

(The consequence if that is not the case isn't huge, it just means memory
would be wasted)
'''

import numpy.random as r
import Queue
import numpy as np
import gzip


class UnigramException(Exception):
	pass


class Unigram(object):

	def __init__(self):
		self.counts = []
		self.total = 0
		self.sampler_ready = False


	def add(self, idx):
		self.sampler_ready = False
		if len(self.counts) <= idx:
			add_zeros = [0] * (idx +1 - len(self.counts))
			self.counts.extend(add_zeros)

		self.counts[idx] += 1


	def update(self, idxs):
		for idx in idxs:
			self.add(idx)

	def make_sampler(self):
		if len(self.counts) < 1:
			raise UnigramException(
				'Cannot sample if no counts have been made'
			)
		self.sampler = MultinomialSampler(self.counts)
		self.sampler_ready = True

	def sample(self, shape=()):
		'''
		Draw a sample according to the unigram probability
		'''
		if not self.sampler_ready:
			self.make_sampler()

		return self.sampler.sample(shape)

	def save(self, filename):
		if filename.endswith('.gz'):
			f = gzip.open(filename, 'w')
		else:
			f = open(filename, 'w')	
		
		for c in self.counts:
			f.write('%d\n' % c)

	def load(self, filename):
		if filename.endswith('.gz'):
			f = gzip.open(filename)
		else:
			f = open(filename)

		self.counts = [int(c) for c in f.readlines()]


	def get_probability(self, token_id):
		'''
		Return the probability associated to token_id.
		'''
		# Delegate to the underlying MultinomialSampler
		if not self.sampler_ready:
			self.make_sampler()
		return self.sampler.get_probability(token_id)



class Node(dict):
	def __cmp__(self, other):
		return cmp(self['count'], other['count'])


class MultinomialSampler(object):

	def __init__(self, scores):
		if len(scores) < 1:
			raise ValueError('The scores list must have length >= 1')
		self.scores = scores
		self.total = float(sum(scores))
		self.K = len(scores)
		self.setup()


	def get_probability(self, k):
		'''
		Get the actual probability associated to outcome k
		'''
		return self.orig_prob_mass[k]


	def setup(self):
		self.orig_prob_mass = np.zeros(self.K)
		self.mixture_prob_mass = np.zeros(self.K)
		self.mass_reasignments = np.zeros(self.K, dtype=np.int64)
 
		# Sort the data into the outcomes with probabilities
		# that are larger and smaller than 1/K.
		smaller = []
		larger  = []
		for k, score in enumerate(self.scores):
			self.orig_prob_mass[k] = score / self.total
			self.mixture_prob_mass[k] = (self.K*score) / self.total
			if self.mixture_prob_mass[k] < 1.0:
				smaller.append(k)
			else:
				larger.append(k)
 
		# We will have k different slots. Each slot represents 1/K
		# prbability mass, and to each we allocate all of the probability
		# mass from a "small" outcome, plus some probability mass from
		# a "large" outcome (enough to equal the total 1/K).
		# We keep track of the remaining mass left for the larger outcome,
		# allocating the remainder to another slot later.
		# The result is that the kth has some mass allocated to outcome
		# k, and some allocated to another outcome, recorded in J[k].
		# q[k] keeps track of how much mass belongs to outcome k, and 
		# how much belongs to outcome J[k].
		while len(smaller) > 0 and len(larger) > 0:
			small_idx = smaller.pop()
			large_idx = larger.pop()
 
			self.mass_reasignments[small_idx] = large_idx
			self.mixture_prob_mass[large_idx] = (
				self.mixture_prob_mass[large_idx] -
				(1.0 - self.mixture_prob_mass[small_idx])
			)
 
			if self.mixture_prob_mass[large_idx] < 1.0:
				smaller.append(large_idx)
			else:
				larger.append(large_idx)
 
		return self.mass_reasignments, self.mixture_prob_mass


	def sample(self, shape=()):

		if len(shape) < 1:
			return self._sample()
		else:
			this_dim = shape[0]
			recurse_shape = shape[1:]
			return np.array(
				[self.sample(recurse_shape) for i in range(this_dim)]
			, dtype='int64')


	def _sample(self):

		# Draw from the overall uniform mixture.
		k = np.int64(int(np.floor(r.rand()*self.K)))
	 
		# Draw from the binary mixture, either keeping the
		# small one, or choosing the associated larger one.
		if r.rand() < self.mixture_prob_mass[k]:
			return k
		else:
			return self.mass_reasignments[k]
 


class SampleTree(object):

	def __init__(self, counts):
		self.counts = counts
		self.root = self.build_tree()



	def build_tree(self):

		# Make leaf nodes for every token count, and put them in the 
		# Queue
		q = Queue.PriorityQueue()
		for idx, count in enumerate(self.counts):
			node = Node([
				('count',count),
				('id', idx),
				('left',None),
				('right',None),
				('prob-left',None)
			])
			q.put(node)


		while True:

			# Take two nodes from the queue
			left = q.get()

			# There might only be one node left
			try:
				right = q.get(block=False) 
			except Queue.Empty:
				break

			# Make a node representing the merging of these
			total_count = left['count']+right['count']
			parent = Node([
				('count', total_count),
				('prob-left', left['count'] / float(total_count)),
				('id',None),
				('left', left),
				('right', right)
			])

			# Now put the merged node itself onto the queue
			q.put(parent)

		# When there's just one node left, it represents the root
		# It will serve as a handle to the tree
		root = left
		return root









