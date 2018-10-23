# First Home Assignment for the Introduction to Data Analysis Class
# See instructions in folder.

########################
# Author: Jernej Vivod #
########################

import csv
import numpy as np
import math
import itertools
from lib_naloga1 import group_distance
from lib_naloga1 import sample_distance
from lib_naloga1 import dendrogram_plotter
from lib_naloga1 import inject
from lib_naloga1 import group_extractor

# Parsing the data file - notes:
"""
	Rows are countries (columns in original file (Q - BK / 17 - 63/) - 47 columns)
	in list comprehension: l[0][16:63] # select names of countries -> keys

	Note that country names are sometimes ended with a space -> trim.

	For each country A:
		- Make bins corresponding to each other country i.
		- In each bin, sum votes from country A for this country i.

	Summing votes for each country i from country A:
		- There are 47 countries voting.
		- Make a tuple of names of countries (column names 17 - 63).
		- Indices of names of countries are also indices in the bins list.
		- Go over all rows representing votes.
		- Get name (and from name, the index) from row name.
		- Add value in row to appropriate bin.
		- Add entry to data dict.
"""

# Read and process data to be used for clustering.
# param file_name: name of the file containing the data
# return: dictionary with element names as keys and feature vectors as values
def read_file(file_name):
	# Open data file
	with open(file_name, "rt", encoding="latin1") as f:
		raw_data = np.array(list(csv.reader(f))) 											# Read lines from csv file into numpy array
		country_names = raw_data[0, 16:63] 													# Get names of countries (as names of rows 17-63)
		country_names = list(map(lambda x: x.strip(), country_names)) 						# Trim whitespace from start and end.
		country_names[country_names.index("Serbia & Montenegro")] = "Serbia and Montenegro" # Handle country name conflict between name in rows and name in columns
		processed_data = dict() 															# Create empty dictionary for storing cleaned data.
		NUM_COUNTRIES = 47 																	# There are 47 countries participating/voting.
		col_names = list(map(lambda x: x.strip(), raw_data[0, :])) 							# Get names of columns.
		col_names[col_names.index("Serbia & Montenegro")] = "Serbia and Montenegro" 		# Handle country name conflict between name in rows and name in columns.
		# Create rows in processed data matrix.
		for country in country_names:
			bins = np.zeros((NUM_COUNTRIES, ), dtype = int) 		# Create bins.
			index_row = col_names.index(country) 					# Get index of column representing votes from this country.

			# Go over performing countries across all years.
			for i in range(1, raw_data.shape[0]):
				bin_index = country_names.index(raw_data[i, 1].strip()) 	# Compute index of bin for next performance
				val = raw_data[i, index_row] 								# Get number of points awarded by country A (If data exists).
				try:
					points = int(val) 								# Try to convert value to an integer.
					bins[bin_index] += points 						# If successfully converted, add to bin.
				except ValueError:
					pass
			processed_data[country] = bins 							# Add country data to dictionary representing the processed data.
		# Return dictionary representing the processed data
		return processed_data

# get_labels: get a 2 by 47 matrix where the first row contains the country names and the second row their regions
# obtained from the third column in the original data sheet.
# This matrix is used as a label for the data matrix obtained by the read_file function (the indices match).
def get_labels(file_name):
	with open(file_name, "rt", encoding="latin1") as f:
		raw_data = np.array(list(csv.reader(f))) 											# Read lines from csv file into numpy array
		country_names = raw_data[0, 16:63] 													# Get names of countries (as names of rows 17-63)
		country_names = list(map(lambda x: x.strip(), country_names)) 						# Trim whitespace from start and end.
		country_names[country_names.index("Serbia & Montenegro")] = "Serbia and Montenegro" # Handle country name conflict between name in rows and name in columns
		country_regions = [] 																# define list that will store regions of countries in country_names list with same index.
		countries = list(raw_data[1:, 1]) 													# All rows of columns with countries and regions (performances)
		regions = raw_data[1:, 2]

		# Make a set of countries that do not appear
		with_unlisted_regions = {"Andorra", "Czech Republic", "Monaco", "Montenegro", "San Marino"} 

		# Get regions for each country.
		for country in country_names:
			if country in with_unlisted_regions:
				country_regions.append("not listed")
			else:
				index_country = countries.index(country) # Get index of country and use it to get region.
				region = regions[index_country]
				country_regions.append(region)

		# Return matrix where the first row contains the country names and the second row their regions
		return np.stack((country_names, country_regions))


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
		self.distances = np.empty((len(self.clusters) - 1,), dtype = list)

		# first_plot: True if the tree has not yet been plotted. This prevents the distance injection functionality
		# to run more than once.
		self.first_plot = True

	# row_distance: compute distance between data in two rows.
	# Example call: self.row_distance("Polona", "Rajko")
	def row_distance(self, r1, r2):

		# use euclidean distance as similarity measure.
		# change value to "manhattan" to use the manhattan distance.
		distance_meas = "euclidean"

		# similarity: check similarity of samples sample_1 and sample_2 using algorithm provided by function func.
		def similarity(sample_1, sample_2, func):
			return func(sample_1, sample_2)

		# Try to read data from specified rows (data accessed by key)
		try:
			r1_data = self.data[r1]
			r2_data = self.data[r2]
		except KeyError("Specified row not found."):
			pass

		# Select distance measuring function to use depending on the value of
		# distance_meas variable.
		distance_func = None
		if distance_meas == "euclidean":
			distance_func = sample_distance.euclidean_dist
		elif distance_meas == "manhattan":
			distance_func = sample_distance.manhattan_dist

		# Compute and return similarity between the rows using the specified distance.
		return distance_func(r1_data, r2_data)

	# cluster_distance: compute distance between two clusters. Each cluster is specified as a list of lists where each list is itself a cluster.
	# Example call: self.cluster_distance([[["Albert"], ["Branka"]], ["Cene"]], [["Nika"], ["Polona"]])
	def cluster_distance(self, c1, c2):
		# Use average linkage as a distance measurement. Change value to
		# "complete" to use complete linkage measurement or use "single" to use single linkage distance measurement.
		distance_meas = "average"

		# Set distance measuring function according to distance_meas variable value.
		distance_func = None
		if distance_meas == "average":
			distance_func = group_distance.average_linkage
		elif distance_meas == "complete":
			distance_func = group_distance.complete_linkage
		elif distance_meas == "single":
			distance_func = group_distance.single_linkage
		elif distance_meas == "ward":
			distance_func = group_distance.ward_distance
		else:
			raise ValueError("Invalid group distance measuring function")
		
		# Compute distance between clusters.
		return distance_func(c1, c2, self.data)


	# Find a pair of closest clusters and returns the pair of clusters and their distance.
	# Example call: self.closest_clusters(self.clusters)
	def closest_clusters(self):

		min_dist = int(1e20) 		# initialize minimal distance to a very large number.
		closest_clusters = None 	# Initialize closest cluster pair to None
		for cluster_pair in itertools.product(self.clusters, self.clusters): 	# Go over pairs of clusters and find pair with minimum distance.
			if cluster_pair[0] != cluster_pair[1]:
				dist = self.cluster_distance(cluster_pair[0], cluster_pair[1])
				if dist < min_dist:
					min_dist = dist
					closest_clusters = cluster_pair

		return closest_clusters, min_dist

	# cluster_union: replace closest clusters in list of clusters with their union. Also append data to the
	# distances list that will be used to inject distances into dendrogram list representation (used for plotting)
	def cluster_union(self, closest_clusters, dist, dist_index):
		cluster1, cluster2 = closest_clusters 			# Get closest clusters.
		self.clusters.remove(cluster1) 					# Remove clusters that will be joined from the list of clusters.
		self.clusters.remove(cluster2)
		new_cluster = [cluster1, cluster2] 				# Create a new cluster representing the union of the removed clusters.
		self.clusters.append(new_cluster) 				# Add union to list of clusters.
		self.distances[dist_index] = [new_cluster, math.ceil(dist) - 27] # Add entry into distances list.


	# Given the data in self.data, performs hierarchical clustering. Can use a while loop, iteratively modify self.clusters and store
	# information on which clusters were merged and what was the distance. Store this later information into a suitable structure to be used
	# for plotting of the hierarchical clustering.
	def run(self):
		dist_index = 0
		# While there is more than one group...
		while(len(self.clusters) > 1):
			closest_clusters, dist = self.closest_clusters() 			# Find closest clusters and their distance.
			# print("Closest clusters with distance {0}.".format(dist)) 	
			self.cluster_union(closest_clusters, dist, dist_index)		# Replace clusters with their union.
			dist_index += 1 											
		self.clusters = self.clusters[0]								# Unnest the final cluster (for plotting)
		

	# Use cluster information to plot an ASCII representation of the cluster tree.
	def plot_tree(self):
		if self.first_plot == True: 									# If first plot, inject distances into list representing the tree.
			inject.inject_distances(self.clusters, self.distances) 		# !!! NOTE: This changes the clusters list. !!!
			self.first_plot = False
		dendrogram_plotter.plot_dendrogram_ascii(self.clusters) 		# Plot dendrogram.


	## AUXILIARY METHODS FOR DATA ANALYSIS AND VISUALIZATION ############################################################

	# run_aux: run clustering algorithm until number of groups is as specified. THIS METHOD IS CALLED BY THE get_groups METHOD.
	def run_aux(self, num_groups):
		dist_index = 0 	# Initialize distance index
		# While there is more than the specified number of groups...
		while(len(self.clusters) > num_groups):
			closest_clusters, dist = self.closest_clusters() 			# Find closest clusters and their distance.
			self.cluster_union(closest_clusters, dist, dist_index)		# Replace clusters with their union.
			dist_index += 1

	# get_groups: method that initializes the instance to appropriate state and then calls the run_aux method.
	def get_groups(self, num_groups):
		self.clusters = [[name] for name in self.data.keys()] 	# Reinitialize clusters.
		self.run_aux(num_groups) 								# Call run_aux method with specified number of groups as argument.

	# extract_group_members: create a new attribute groups which is a dict that maps group indices to a list of countries in the group.
	def extract_group_members(self):
		groups = dict()
		for index, group in enumerate(self.clusters):
			groups[index] = group_extractor.extract_names(group) 	# Extract names from specified group and map group index to list of country names.
		self.groups = groups 										# Make groups dict an instance attribute.

	########################################################################################################################


# If running this file as a script
if __name__ == "__main__":

	# Read data.
	DATA_FILE = "eurovision-final.csv"

	# Create a HierarchicalClustering instance initialized with parsed data.
	hc = HierarchicalClustering(read_file(DATA_FILE))

	# Perform clustering
	hc.run()

	# Plot results of clustering.
	hc.plot_tree()