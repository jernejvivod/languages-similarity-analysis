########################
# Author: Jernej Vivod #
########################
import numpy as np
import math
import itertools
from lib_HClustering import group_similarity
from lib_HClustering import dendrogram_plotter
from lib_HClustering import inject
from lib_naloga2 import document_comparator

# HierarchicalClustering: class implementing hierarchical clustering functionalities
class HierarchicalClustering:

	# constructor: assign parsed data and create initial clusters where each row is its own data.
	def __init__(self, data):
		# Initialize clustering
		self.data = data

		# self.clusters stores current clustering.
		self.clusters = [[name] for name in self.data.keys()]

		# distances: A list that maps each cluster to the distance between its two nested clusters
		# This list is used to inject distances into list representing the dendrogram to allow
		# the plotting of a proportional dendrogram.
		self.similarities = np.empty((len(self.clusters) - 1,), dtype = list)

		# first_plot: True if the tree has not yet been plotted. This prevents the distance injection functionality
		# to run more than once.
		self.first_plot = True

	# row_similarity: compute distance between data in two rows.
	# Example call: self.row_similarity("doc1.txt", "doc2.txt")
	def row_similarity(self, r1, r2):

		# Try to read data from specified rows (data accessed by key)
		try:
			r1_data = self.data[r1]
			r2_data = self.data[r2]
		except KeyError("Specified row not found."):
			pass

		# Compute and return similarity between the rows.
		return document_comparator.document_cosine_sim2(r1_data, r2_data)

	# cluster_similarity: compute distance between two clusters. Each cluster is specified as a list of lists where each list is itself a cluster.
	def cluster_similarity(self, c1, c2):
		# Compute similarity between clusters.
		return group_similarity.average_linkage(c1, c2, self.data)


	# Find a pair of closest clusters and returns the pair of clusters and their distance.
	# Example call: self.closest_clusters(self.clusters)
	def closest_clusters(self):
		max_sim = -1 				# initialize minimal distance to a very large number.
		closest_clusters = None 	# Initialize closest cluster pair to None
		for cluster_pair in itertools.product(self.clusters, self.clusters): 	# Go over pairs of clusters and find pair with minimum distance.
			if cluster_pair[0] != cluster_pair[1]:
				sim = self.cluster_similarity(cluster_pair[0], cluster_pair[1])
				if sim > max_sim:
					max_sim = sim
					closest_clusters = cluster_pair

		return closest_clusters, max_sim

	# cluster_union: replace closest clusters in list of clusters with their union. Also append data to the
	# distances list that will be used to inject distances into dendrogram list representation (used for plotting)
	def cluster_union(self, closest_clusters, sim, sim_index):
		cluster1, cluster2 = closest_clusters 			# Get closest clusters.
		self.clusters.remove(cluster1) 					# Remove clusters that will be joined from the list of clusters.
		self.clusters.remove(cluster2)
		new_cluster = [cluster1, cluster2] 				# Create a new cluster representing the union of the removed clusters.
		self.clusters.append(new_cluster) 				# Add union to list of clusters.
		self.similarities[sim_index] = [new_cluster, math.ceil(((1 - sim)**4) * 100)] # Add entry into distances list.


	# Given the data in self.data, performs hierarchical clustering. Can use a while loop, iteratively modify self.clusters and store
	# information on which clusters were merged and what was the distance. Store this later information into a suitable structure to be used
	# for plotting of the hierarchical clustering.
	def run(self):
		sim_index = 0
		# While there is more than one group...
		while(len(self.clusters) > 1):
			print("Current number of clusters: {0}".format(len(self.clusters)))
			closest_clusters, sim = self.closest_clusters() 			# Find closest clusters and their distance.
			self.cluster_union(closest_clusters, sim, sim_index)		# Replace clusters with their union.
			sim_index += 1 											
		self.clusters = self.clusters[0]								# Unnest the final cluster (for plotting)
		

	# Use cluster information to plot an ASCII representation of the cluster tree.
	def plot_tree(self):
		if self.first_plot == True: 									# If first plot, inject distances into list representing the tree.
			inject.inject_similarities(self.clusters, self.similarities) 		# !!! NOTE: This changes the clusters list. !!!
			self.first_plot = False
		print('\n')
		dendrogram_plotter.plot_dendrogram_ascii(self.clusters) 		# Plot dendrogram.