import random
from lib_naloga2 import document_comparator


class KMclustering:
	def __init__(self, document_vectors):
		# Document vectors represented as a dictionary.
		self.document_vectors = document_vectors
		# Set that contains the names of documents that are currently selected as the medoids.
		self.medoids = set()
		# dictionary that maps document vector keys to document vector keys representing the medoid to which
		# the document vector is associated.
		self.associations = dict()

	def initialize_medoids(self, num_medoids):
		vectors_set = set(self.document_vectors.keys())
		self.medoids = set(random.sample(vectors_set, num_medoids))


	def associate_with_medoids(self):
		for key in [key for key in self.document_vectors.keys() if key not in self.medoids]:
			min_dist = 10e6
			closest_medoid = None
			for medoid in self.medoids:
				dist = document_comparator.document_cosine_sim(self.document_vectors[key], self.document_vectors[medoid])
				if dist < min_dist:
					min_dist = dist
					closest_medoid = medoid
			self.associations[key] = closest_medoid

	def run(self, num_medoids):
		self.initialize_medoids(num_medoids)
		self.associate_with_medoids()
		# Emulate a do-while loop.
		while True:
			for medoid in self.medoids:
				for non_medoid in self.associations.keys():
					# swap medoid and nonmedoid

					# Recompute the cost (sum of distances of points to their medoid).

					# If the total cost of the configuration increased in the previous step, undo the swap.