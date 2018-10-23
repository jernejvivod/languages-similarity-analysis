import itertools
import numpy as np
from lib_HClustering import nesttools
from lib_naloga2 import document_comparator

########################
# Author: Jernej Vivod #
########################

# average_linkage: return average distance between samples in group c1 and samples in group c2.
def average_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1)) # Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))
	prod = itertools.product(c1_elements, c2_elements) 	# Get cartesian product of elements from the groups.

	# Create accumulator for measuring the sum of distances of pairs in cartesian product.
	total_sim = 0
	for pair in prod:
		pair_fst_data = data[pair[0]] # Get data for countries in pair.
		pair_snd_data = data[pair[1]]
		sim = document_comparator.document_cosine_sim2(pair_fst_data, pair_snd_data) # Compute distance and add to total.
		total_sim += sim

	# Return average distance between elements of groups.
	return total_sim / (len(c1_elements) * len(c2_elements))