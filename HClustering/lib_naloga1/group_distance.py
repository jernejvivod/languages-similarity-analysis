import itertools
import numpy as np
from lib_naloga1 import sample_distance
from lib_naloga1 import nesttools

########################
# Author: Jernej Vivod #
########################

# average_linkage: return average distance between samples in group c1 and samples in group c2.
def average_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1)) # Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))
	prod = itertools.product(c1_elements, c2_elements) 	# Get cartesian product of elements from the groups.

	# Create accumulator for measuring the sum of distances of pairs in cartesian product.
	total_dist = 0
	for pair in prod:
		pair_fst_data = data[pair[0]] # Get data for countries in pair.
		pair_snd_data = data[pair[1]]
		dist = sample_distance.euclidean_dist(pair_fst_data, pair_snd_data) # Compute distance and add to total.
		total_dist += dist

	# Return average distance between elements of groups.
	return total_dist / (len(c1_elements) * len(c2_elements))
		
# complete_linkage: return maximal distance between two samples where first sample is in group c1 and second sample in group c2.
def complete_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1))	# Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))

	# Get list of of data for each country in each group.
	c1_data = list(map(lambda x: data[x], c1_elements))
	c2_data = list(map(lambda x: data[x], c2_elements))

	# Initialize max distance to 0.
	max_dist = 0

	# Find max distance between samples in different groups.
	for c1_sample in c1_data:
		for c2_sample in c2_data:
			dist = sample_distance.euclidean_dist(c1_sample, c2_sample)
			if dist > max_dist: 			# If distance is new maximal distance...
				max_dist = dist

	# Return found maximal distance
	return max_dist

# single_linkage: return minimal distance between two samples where first sample is in group c1 and second sample in group c2.
def single_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1)) # Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))

	# Get list of of data for each country in each group.
	c1_data = list(map(lambda x: data[x], c1_elements))
	c2_data = list(map(lambda x: data[x], c2_elements))

	# Initialize min distance to a very large value.
	min_dist = int(1e20)

	# Find max distance between samples in different groups.
	for c1_sample in c1_data:
		for c2_sample in c2_data:
			dist = sample_distance.euclidean_dist(c1_sample, c2_sample)
			if dist < min_dist: 	# If distance is new minimal distance...
				min_dist = dist

	# Return found maximal distance
	return min_dist

# ward_distance: compute ward distance between clusters c1 and c2.
def ward_distance(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1))	# Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))

	# Get list of of data for each country in each group.
	c1_data = list(map(lambda x: data[x], c1_elements))
	c2_data = list(map(lambda x: data[x], c2_elements))

	# Find centroids of c1 and c2 (average of samples in groups).
	Rc1 = np.zeros(47, dtype = int)
	for el in c1_data:
		Rc1 = np.add(Rc1, el)
	Rc1 = np.true_divide(Rc1, len(c1_data))

	Rc2 = np.zeros(47, dtype = int)
	for el in c2_data:
		Rc2 = np.add(Rc2, el)
	Rc2 = np.true_divide(Rc2, len(c2_data))

	# Find centroid of union(c1 c2) (average of samples in union).
	Rc1c2 = np.zeros(47, dtype = int)
	for el in np.concatenate([c1_data, c2_data]):
		Rc1c2 = np.add(Rc1c2, el)
	Rc1c2 = np.true_divide(Rc1c2, len(np.concatenate([c1_data, c2_data])))


	# Compute and return ward distance using formula. 
	sum_1 = 0
	for el in np.concatenate([c1_data, c2_data]):
		sum_1 += sample_distance.manhattan_dist(el, Rc1c2)**2

	sum_2 = 0
	for el in c1_data:
		sum_2 += sample_distance.manhattan_dist(el, Rc1)**2
	
	sum_3 = 0
	for el in c2_data:
		sum_3 += sample_distance.manhattan_dist(el, Rc2)**2

	return sum_1 - (sum_2 + sum_3)