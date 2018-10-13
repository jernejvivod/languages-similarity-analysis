import math
import triplet_extractor

# count_containing: count number of documents that contain specified triplet and return result.
def count_containing(results_dict, triplet):
	counter = 0 		# Initialize counter.
	for doc in results_dict.keys(): 		# Go over documents.
		if triplet in set(results_dict[doc].keys()): 	# If triplet contained in unique set of triplets found in document,
			counter +=1 								# increment counter.
	return counter


# documents_to_vectors: take a list of document names and return dict that maps
# document names to their attribute vectors computed using triplets found in documents and their
# frequencies and inverse document frequencies
#
# The vectors representing each document are represented as dictionaries.
def documents_to_vectors(documents):
	results_dict = dict()					# Define dictionary for storing the results.
	triplets_global = set() 				# Define matrix for storing unique triplets found in all documents.

	# Go over documents in list of document names.
	for document in documents:
		document_text = open("./data/translations/fin.txt", encoding="utf8").read() 	# Parse document
		# Get dictionary that maps unique triplets to their relative frequencies
		triplets_dict = triplet_extractor.text_to_triplets_dict(text)
		triplets_global |= set(list(triplets_dict.keys())) 			# Add found unique triplets to global set of unique triplets
		results_dict[document] = triplets_dict

	# Compute inverse document frequency for each triplet in global set of unique triplets.
	idf_dict = dict() 				# Define dictionary that maps each triplet to its idf.
	num_documents = len(documents)
	for triplet in triplets_global:
		# Count number of documents in which the triplet appears.
		num_containing = count_containing(results_dict, triplet)
		# Compute inverse document frequency.
		idf_dict[triplet] = math.log(num_documents / num_containing)

	# Multiply relative frequencies in document vectors with the triplet's inverse document frequency.
	for document in documents: 							# Go over documents.
		for triplet in results_dict[document].keys(): 	# Go over triplets in next document.
			results_dict[document][key] *= idf_dict[triplet] 	# Multiply relative frequency of triplet with its idf.
"""

When computing vector representation of two documents for distance computations,
we only need to consider the triplets that appear in at least one of the two documents.
If a triplet appears only in one of the two documents, simply put a 0 at this index in the vector
for the other vector. There is no need to pad the vectors with 0's for triplets that do not appear in
either documents as the distance will not change in any way.

a1 = [1, 2, 0, 3, 0, 5]
b1 = [3, 0, 2, 4, 1, 0]

a2 = [1, 2, 0, 3, 0, 5, 0, 0, 0, 0, 0, ...]
b2 = [3, 0, 2, 4, 1, 0, 0, 0, 0, 0, 0, ...]

% distance between a1 and b1 is equal to the distance between a2 and b2.

r1 = dot(a1, b1)/(norm(a1)* norm(b1))
r2 = dot(a2, b2)/(norm(a2)* norm(b2))

r1 == f2 -> TRUE

"""