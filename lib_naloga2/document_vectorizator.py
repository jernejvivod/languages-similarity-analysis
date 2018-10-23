import math
from lib_naloga2 import triplet_extractor
from joblib import Parallel, delayed
import multiprocessing

########################
# Author: Jernej Vivod #
########################

# count_containing: count number of documents that contain specified triplet and return result.
def count_containing(results_dict, triplet):
	counter = 0 		# Initialize counter.
	for doc in results_dict.keys(): 		# Go over documents.
		if triplet in set(results_dict[doc].keys()): 	# If triplet contained in unique set of triplets found in document,
			counter +=1 								# Increment counter.
	return counter


# documents_to_vectors: take a list of document names and return dict that maps
# document names to their attribute vectors computed using triplets found in documents and their
# frequencies and inverse document frequencies
#
# The vectors representing each document are represented as dictionaries.
def documents_to_vectors(documents, documents_path, compute_idfs = True):
	results_dict = dict()					# Define dictionary for storing the results.
	triplets_global = set() 				# Define matrix for storing unique triplets found in all documents.

	# Go over documents in list of document names.
	for document in documents:
		print("Vectorizing '{0}'...".format(document))
		document_text = open(documents_path + document, encoding="utf8").read() 	# Parse document
		# Get dictionary that maps unique triplets to their relative frequencies
		triplets_dict = triplet_extractor.text_to_triplets_dict(document_text)
		triplets_global |= set(list(triplets_dict.keys())) 			# Add found unique triplets to global set of unique triplets
		results_dict[document] = triplets_dict

	if compute_idfs:
		print('Computing idf values...')
		# Compute inverse document frequency for each triplet in global set of unique triplets.
		idf_dict = multiprocessing.Manager().dict() 	# Define dictionary that maps each triplet to its idf.
		num_documents = len(documents)

		# compute_idfs: compute idf value for each triplet found in any of the documents and add
		# entry to dictionary. This function is used in a parallelized loop implemented below.
		def compute_idfs(triplet):
			# Count number of documents in which the triplet appears.
			num_containing = count_containing(results_dict, triplet)
			# Compute inverse document frequency.
			idf_dict[triplet] = math.log(num_documents / num_containing)

		# Get number of cores on system.
		num_cores = multiprocessing.cpu_count()
		# Compute idf values in a parallelized loop.
		Parallel(n_jobs=num_cores)(delayed(compute_idfs)(triplet) for triplet in triplets_global)

		# Multiply relative frequencies in document vectors with the triplet's inverse document frequency.
		for document in documents: 							# Go over documents.
			for triplet in results_dict[document].keys(): 	# Go over triplets in next document.
				results_dict[document][triplet] *= idf_dict[triplet] 	# Multiply relative frequency of triplet with its idf.
	
	return results_dict