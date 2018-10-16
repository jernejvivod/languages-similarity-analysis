import random
from lib_naloga2 import document_comparator

class KMclustering:

	def __init__(self, document_vectors):
		# Document vectors represented as a dictionary.
		self.document_vectors = document_vectors
		# Set that contains the names of documents that are currently selected as the medoids.
		self.medoids = set()

		# See run method.
		self.associations = dict()
		self.arrangement_cost = 0

	# initialize_medoids: select medoids from document vectors by sampling from pool.
	def initialize_medoids(self, num_medoids):
		vectors_set = set(self.document_vectors.keys()) 			# Create a pool.
		self.medoids = set(random.sample(vectors_set, num_medoids)) # Sample.

	# associate_with_medoids: associate ever non-medoid vector with closest medoid.
	def associate_with_medoids(self, medoids):
		associations = dict() 					# associations: dict that maps document names to document names of their associated medoids.
		for key in [key for key in self.document_vectors.keys() if key not in medoids]: # Go over non-medoid vectors.
			min_dist = -1
			closest_medoid = None
			for medoid in medoids: 														# Find closest medoid.
				dist = document_comparator.document_cosine_sim(self.document_vectors[key], self.document_vectors[medoid])
				if dist > min_dist:
					min_dist = dist
					closest_medoid = medoid
			associations[key] = closest_medoid
		return associations

	# compute_arrangement_cost: compute sum of similarity coefficients in current arrangement of medoids.
	def compute_arrangement_cost(self, associations):
		cost = 0
		for vect in associations.keys(): # Go over non-medoid vectors and add similarity coefficient to total sum.
			cost += document_comparator.document_cosine_sim(self.document_vectors[vect], self.document_vectors[associations[vect]])
		return cost

	# run: perform k-medoid clustering. This method computes values for two attributes of invoking instance. associations is a dictionary
	# that maps names of vectors to names of their associated medoids. arrangement_cost is the total sum of the similarity coefficients
	# between vectors and their medoids in the given arrangement.
	def run(self, num_medoids):
		self.initialize_medoids(num_medoids) 	# Initialize medoids by random sampling from pool.
		associations = self.associate_with_medoids(self.medoids) 	# Associate non-medoid vectors with their medoids.
		arrangement_cost = self.compute_arrangement_cost(associations) 	# Compute cost of current arrangement.
		print("initial cost: {0}".format(arrangement_cost)) 		
		improvement = True 											# Loop while cost is improving.
		while improvement:
			improvement = False
			for medoid in self.medoids: 							# For each medoid.
				for non_medoid in associations.keys(): 				# Go over each non-medoid.
					medoids_alt = self.medoids.copy() 				# Create alternative set of medoids with current medoid and non_medoid swapped.
					medoids_alt.remove(medoid)
					medoids_alt.add(non_medoid)
					associations_alt = self.associate_with_medoids(medoids_alt) 	# Associate non-medoids to medoids in this new arrangement.
					new_cost = self.compute_arrangement_cost(associations_alt) 	# Compute new similarity coefficient sum.
					if new_cost > arrangement_cost: 							# If similarity coefficient sum is greate, keep arrangement. 
						print('higher cost: {0}'.format(new_cost))
						arrangement_cost = new_cost
						self.medoids = medoids_alt
						associations = associations_alt
						improvement = True
						break
				else: 			# If inner loop DID NOT BREAK, continue with next iteration of outer loop.
					continue
				break 			# If inner loop DID BREAK, break outer loop (repeat computations for new arrangement).
		self.associations = associations 			# Create new attributes.
		self.arrangement_cost = arrangement_cost
