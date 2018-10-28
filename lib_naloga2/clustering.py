import random
import numpy as np
from matplotlib import pyplot as plt
from lib_naloga2 import document_comparator
########################
# Author: Jernej Vivod #
########################

# KMclustering: class that implements methods used to perform the k-medians clustering algorithm.
class KMclustering:
	def __init__(self, document_vectors):
		# Document vectors represented as a dictionary.
		self.document_vectors = document_vectors
		# Set that contains the names of documents that are currently selected as the medoids.
		self.medoids = set()
		# See run method.
		self.associations = dict()
		self.arrangement_cumsim = 0
		self.sim_matrix = dict()  # Dictionary that maps each pair of document vectors to their similarity.
		# dictionary that maps each document name to its silhouette value.
		self.silhouettes = dict()
		self.clustering_silhouette = 0 # Average silhouette value in iteration.

	# initialize_medoids: select medoids from document vectors by sampling from pool.
	def initialize_medoids(self, num_medoids):
		vectors_set = set(self.document_vectors.keys()) 			# Create a pool.
		self.medoids = set(random.sample(vectors_set, num_medoids)) # Sample.
		# Compute distances of each vector to every other vector.
		for vect in self.document_vectors:  # Go over pairs of vectors.Najbrž ni normalno, da zadeva pri vsaki inicializaciji medoidov skonvergira v isto stvar, da imam potem vse vrednosti silhuet 
			for other_vect in self.document_vectors:
				if vect != other_vect: 		# Do not compare vectors with themselves.
					sim = document_comparator.document_cosine_sim(self.document_vectors[vect], self.document_vectors[other_vect])
					self.sim_matrix[(vect, other_vect)] = sim  # Add distance between vectors to similarity matrix (represented as a dict).

	# associate_with_medoids: associate ever non-medoid vector with closest medoid.
	def associate_with_medoids(self, medoids):
		associations = dict() 					# associations: dict that maps document names to document names of their associated medoids.
		for key in [key for key in self.document_vectors.keys() if key not in medoids]: # Go over non-medoid vectors.
			min_sim = -1
			closest_medoid = None
			for medoid in medoids: 														# Find closest medoid.
				sim = self.sim_matrix[key, medoid]
				if sim > min_sim:
					min_sim = sim
					closest_medoid = medoid
			associations[key] = closest_medoid
		return associations

	# compute_arrangement_cumsim: compute sum of similarity coefficients in current arrangement of medoids.
	def compute_arrangement_cumsim(self, associations):
		cumsim = 0
		for vect in associations.keys(): # Go over non-medoid vectors and add similarity coefficient to total sum.
			cumsim += self.sim_matrix[vect, associations[vect]]
		return cumsim

	# get_silhouettes: compute silhouette values for current arrangement.
	def get_silhouettes(self):
		# Go over document vectors and compute their silhouettes.
		for doc in self.document_vectors.keys():
			# Compute sum of distances to documents associated with clusters of which doc is not a member.
			# Get set of documents that are not in same cluster.
			if doc not in self.medoids:
				doc_assoc = self.associations[doc];
			else:
				doc_assoc = doc

			# Make set of documents that are in the same cluster and set of documents that are not in the same cluster.
			docs_in_other_clusters = set();
			docs_in_same_cluster = set()
			# Go over documents.
			for doc_other in self.document_vectors.keys():
				# If documents are equal, ignore.
				if doc_other == doc:
					pass
				# If document is a medoid...
				elif doc_other in self.medoids:
					# ...If it is the same as the mediod with which the current document is associated, add
					# to set of documents in same cluster. Else add to set of documents in other clusters.
					if doc_other == doc_assoc:
						docs_in_same_cluster.add(doc_other)
					else:
						docs_in_other_clusters.add(doc_other)
				# If document is not associated with same medoid, add to set of documents in other clusters.
				elif self.associations[doc_other] != doc_assoc:
					docs_in_other_clusters.add(doc_other)
				# Else, document is associated with same medoid. Add to set of documents in same cluster.
				else:
					docs_in_same_cluster.add(doc_other)
			
			# Compute average similarity to documents in same cluster and average similarity to documents in other clusters.
			average_sim_other = 0
			average_sim_same = 0
			# Add similarity values to cummulative sums..
			for e in docs_in_other_clusters:
				average_sim_other += self.sim_matrix[doc, e]
			for e in docs_in_same_cluster:
				average_sim_same += self.sim_matrix[doc, e]
			# Compute average similarities. Handle possible division by zero.
			average_sim_other = average_sim_other / len(docs_in_other_clusters) if len(docs_in_other_clusters) > 0 else 0
			average_sim_same = average_sim_same / len(docs_in_same_cluster) if len(docs_in_same_cluster) > 0 else 0
			# Set silhouette value and handle possible division with zero that occur when handling languages orthogonal to every other language.
			self.silhouettes[doc] = ((1-average_sim_other) - (1-average_sim_same))/max((1 - average_sim_other), (1 - average_sim_same))

	# plot_silhouettes: make and display a silhouette plot for the current arrangement.
	def plot_silhouettes(self, colors):
		plt.clf()
		plt.cla()

		# Get members of each cluster as a list of lists.
		groups = dict((key, [key]) for key in self.medoids) 	# Make sure to add medoid to group.
		for assoc in self.associations.keys():
			groups[self.associations[assoc]].append(assoc) 				# Add node associated with medoid to group.
		clusters = list(groups.values())

		# Initialize horizontal bar plot with dummy values.
		b = plt.barh(range(len(self.document_vectors)), [1 for k in range(len(self.document_vectors))])
		ax = plt.gca()

		# Define an empty list for storing cluster lengths in correct order (used for centering plot ticks.)
		cluster_idx_centers = []

		# Go over each cluster and plot it on bar plot
		vect_idx = 0  # Index of vector.
		col_idx = 0   # Index of color.
		# Go over clusters.
		for cluster in clusters:
			# Get silhuette values in cluster and sort tem in descending order.
			cluster_silhouettes = list(map(lambda x: self.silhouettes[x], cluster))
			cluster_silhouettes.sort(reverse = True)
			# Add size of cluster to list of sizes (used for plot tick centering).
			cluster_idx_centers.append(len(cluster_silhouettes))
			# Set bar height and color for corresponding vector.
			for val in cluster_silhouettes:
				b[len(b) - 1 - vect_idx].set_width(val)
				b[len(b) - 1 - vect_idx].set_color(colors[col_idx])
				vect_idx += 1  # Increment vector index.
			col_idx += 1  # Increment color index.

		# Get on plot at start of each cluster.
		cluster_idx_centers_cs = np.cumsum(list(reversed(cluster_idx_centers)))
		# Perform centering by subtracting halves of lengths of clusters from each starting point.
		ticks = np.subtract(cluster_idx_centers_cs, list(reversed(np.divide(cluster_idx_centers, 2))))

		# Create ticks.
		tick_vals = list(range(len(self.medoids)))
		tick_vals = list(map(lambda x: 'Cluster ' + str(x), tick_vals))

		# Add ticks and title to plot and show plot.
		ax.set_yticks(ticks)
		ax.set_yticklabels(tick_vals)
		plt.xlabel('Silhouette value')
		plt.show(block=False)
		plt.pause(0.02)


	# run: perform k-medoid clustering. This method computes values for two attributes of invoking instance. associations is a dictionary
	# that maps names of vectors to names of their associated medoids. arrangement_cumsum is the total sum of the similarity coefficients
	# between vectors and their medoids in the given arrangement.
	def run_exhaustive(self, num_medoids):
		self.initialize_medoids(num_medoids) 	# Initialize medoids by random sampling from pool.
		associations = self.associate_with_medoids(self.medoids) 	# Associate non-medoid vectors with their medoids.
		arrangement_cumsim = self.compute_arrangement_cumsim(associations) 	# Compute cummulative similarity of current arrangement.
		improvement = True 											# Loop while cummulative similarity is improving.
		while improvement:
			improvement = False
			for medoid in self.medoids: 							# For each medoid.
				for non_medoid in associations.keys(): 				# Go over each non-medoid.
					medoids_alt = self.medoids.copy() 				# Create alternative set of medoids with current medoid and non_medoid swapped.
					medoids_alt.remove(medoid)
					medoids_alt.add(non_medoid)
					associations_alt = self.associate_with_medoids(medoids_alt) 	# Associate non-medoids to medoids in this new arrangement.
					new_cumsim = self.compute_arrangement_cumsim(associations_alt) 	# Compute new similarity coefficient sum.
					if new_cumsim > arrangement_cumsim: 							# If similarity coefficient sum is greate, keep arrangement. 
						arrangement_cumsim = new_cumsim
						self.medoids = medoids_alt
						associations = associations_alt
						improvement = True
						break
				else: 			# If inner loop DID NOT BREAK, continue with next iteration of outer loop.
					continue
				break 			# If inner loop DID BREAK, break outer loop (repeat computations for new arrangement).
		self.associations = associations 			# Assign attributes.
		self.arrangement_cumsim = arrangement_cumsim  # Assign commulative value of arrangement similarities.
		self.get_silhouettes() 						  # Compute arrangement silhouettes for each document.
		self.clustering_silhouette = sum(self.silhouettes.values())/len(self.silhouettes.values())  # Compute average silhouette



	# run: perform k-medoid clustering. This method computes values for two attributes of invoking instance. associations is a dictionary
	# that maps names of vectors to names of their associated medoids. arrangement_cumsum is the total sum of the similarity coefficients
	# between vectors and their medoids in the given arrangement.
	def run_greedy(self, num_medoids):
		self.initialize_medoids(num_medoids) 	# Initialize medoids by random sampling from pool.
		associations = self.associate_with_medoids(self.medoids) 	# Associate non-medoid vectors with their medoids.
		arrangement_cumsim = self.compute_arrangement_cumsim(associations) 	# Compute cummulative similarity of current arrangement.
		for medoid in self.medoids: 							# For each medoid.
			for non_medoid in associations.keys(): 				# Go over each non-medoid.
				medoids_alt = self.medoids.copy() 				# Create alternative set of medoids with current medoid and non_medoid swapped.
				medoids_alt.remove(medoid)
				medoids_alt.add(non_medoid)
				associations_alt = self.associate_with_medoids(medoids_alt) 	# Associate non-medoids to medoids in this new arrangement.
				new_cumsim = self.compute_arrangement_cumsim(associations_alt) 	# Compute new similarity coefficient sum.
				if new_cumsim > arrangement_cumsim: 							# If similarity coefficient sum is greate, keep arrangement. 
					arrangement_cumsim = new_cumsim
					self.medoids = medoids_alt
					associations = associations_alt
					break
			else: 			# If inner loop DID NOT BREAK, continue with next iteration of outer loop.
				continue
			break 			# If inner loop DID BREAK, break outer loop (repeat computations for new arrangement).
		self.associations = associations 			# Assign attributes.
		self.arrangement_cumsim = arrangement_cumsim  # Assign commulative value of arrangement similarities.
		self.get_silhouettes() 						  # Compute arrangement silhouettes for each document.
		self.clustering_silhouette = sum(self.silhouettes.values())/len(self.silhouettes.values())  # Compute average silhouette