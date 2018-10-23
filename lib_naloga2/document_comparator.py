import math
import numpy as np
########################
# Author: Jernej Vivod #
########################

"""

When computing vector representation of two documents for distance computations,
we only need to consider the triplets that appear in at least one of the two documents.
If a triplet appears only in one of the two documents, simply put a 0 at this index in the vector
for the other vector. There is no need to pad the vectors with 0's for triplets that do not appear in
either documents as the distance will not change in any way.

a1 = [1, 2, 0, 3, 0, 5];
b1 = [3, 0, 2, 4, 1, 0];

a2 = [1, 2, 0, 3, 0, 5, 0, 0, 0, 0, 0, ...];
b2 = [3, 0, 2, 4, 1, 0, 0, 0, 0, 0, 0, ...];

% distance between a1 and b1 is equal to the distance between a2 and b2.

r1 = dot(a1, b1)/(norm(a1)* norm(b1));
r2 = dot(a2, b2)/(norm(a2)* norm(b2));

r1 == f2 -> TRUE

% Note also that distances between:

a = [1, 2, 3];
b = [2, 3, 4];

% are the same as between:

a = [2, 1, 3];
b = [3, 2, 4];

% (Same permutation applied to both vectors)

"""

# document_cosine_sim: compute cosine similarity between two documents using cosine similarity.
# The function takes dictionaries that map triplets found in each document to its tf-idf value.
def document_cosine_sim(doc_dict1, doc_dict2):
	dot_product = sum(doc_dict1[key]*doc_dict2.get(key, 0) for key in doc_dict1.keys()) # Compute dot product.
	norm_1 = math.sqrt(sum(doc_dict1[key]**2 for key in doc_dict1.keys())) 				# Compute norms.
	norm_2 = math.sqrt(sum(doc_dict2[key]**2 for key in doc_dict2.keys()))
	return dot_product/(norm_1 * norm_2) # Compute and return cosine similarity.


## Functions used with hierarchical clustering algorithm ###########################################################################

# doc_dicts_to_vects: transform doc_dict1 and doc_dict2 to appropriate vectors.
# See above notes for more information.
# This function is used to transform document vectors to form that is compatible with the hierarchical clustering algorithm.
def doc_dicts_to_vects(doc_dict1, doc_dict2):
	# Define set of all triplets found in either document.
	triplets_all = set(doc_dict1.keys()) | set(doc_dict2.keys())
	# Allocate memory for vectors
	vect1 = np.empty(len(triplets_all), dtype=float) 
	vect2 = np.empty(len(triplets_all), dtype=float)
	# Go over enumerated triplets.
	for idx, triplet in enumerate(triplets_all):
		if triplet in doc_dict1: 	# If triplet found in first document, add its tf-id value vector.
			vect1[idx] = doc_dict1[triplet]
		else:
			vect1[idx] = 0 			# Else add zero entry.
		if triplet in doc_dict2:
			vect2[idx] = doc_dict2[triplet]
		else:			
			vect2[idx] = 0
	return vect1, vect2 			# Return created vectors in order.

# document_cosine_sim: compute cosine similarity between two documents using cosine similarity.
# The function takes dictionaries that map triplets found in each document to its tf-idf value.
def document_cosine_sim2(doc_dict1, doc_dict2):
	vect1, vect2 = doc_dicts_to_vects(doc_dict1, doc_dict2)  					# Get vector representations of the two documents.
	return np.dot(vect1, vect2)/(np.linalg.norm(vect1) * np.linalg.norm(vect2)) # Compute and return cosine similarity.

######################################################################################################################################