import numpy as np
from lib_naloga2 import document_vectorizator, document_comparator
from matplotlib import pyplot as plt

########################
# Author: Jernej Vivod #
########################

# LaguageAnalyzer: class that implements methods used to deduce the most probable language of a text document.
class LanguageAnalyzer:
	# Initialize with dictionary containing vectors of reference documents and with dictionary
	# for decoding the OHCHR language codes to English names.
	def __init__(self, reference_triplets_dicts, decode_OHCHR):
		self.reference_triplets_dicts = reference_triplets_dicts
		self.decode_OHCHR = decode_OHCHR

	# document_to_triplets_dict: convert document with name document_name and
	# documents_path as the path to the folder in which the document is located.
	def document_to_triplets_dict(self, document_name, documents_path):
		# Get triplets dict for document with name document_name.
		res = document_vectorizator.documents_to_vectors([document_name], documents_path, False);
		return res[document_name]  # there is only one document in the dictionary returned by documents_to_vectors method. Return it.

	# similarities_to_references: compute similarities of obtained document vector to reference vectors.
	# return a dictionary that maps cosine similarities to language names decoded from OHCHR codes.
	def similarities_to_references(self, document_triplets_dict):
		# Compute cosine similarities of computed vector with vectors obtained from documents in known languages.
		similarities = dict()
		for reference in self.reference_triplets_dicts.keys(): 	# Go over reference documents.
			sim = document_comparator.document_cosine_sim(self.reference_triplets_dicts[reference], document_triplets_dict)
			similarities[sim] = self.decode_OHCHR[reference[:-4]] 	# Add result to dictionary.
		return similarities

	# display_first_k: display the first k most likely languages for document with its similarity dictionary
	# as the function parameter.
	def display_first_k(self, k, similarities_dict):
		sim_coeffs = list(similarities_dict.keys())  # Make a list of cosine similarity values.
		sim_coeffs.sort(reverse = True) 			 # Sort cosine similarities in descending order.
		print('###################################################################################')
		print('# Suggested Languages for This Document Based on Cosine Similarity to References: #')
		print('###################################################################################')
		for i in range(k): 	# Print k most likely languages for this document.
			line = '{0}. {1} '.format(i + 1, similarities_dict[sim_coeffs[i]])
			sub_padding = len(line)
			line += '{0: >{width}}'.format('(cosine similarity = {0})'.format(round(sim_coeffs[i], 3)), width = 50 - sub_padding)
			print(line)
		# Plot results as a horizontal bar graph.
		plt.barh(list(reversed([similarities_dict[sim] for sim in sim_coeffs[:k]])), list(reversed(sim_coeffs[:k])), color = 'skyblue')
		plt.title('Suggested Languages for This Document Based on\n Cosine Similarity to References')
		plt.xlabel('Cosine Similarity')
		plt.show()
		

	# run: find num_most_similar language suggestions for document with name document_name and document_path as the
	# path to the documents folder.
	def run(self, num_most_similar, document_name):
		document_triplets_dict = self.document_to_triplets_dict(document_name, './data/language_analysis_data/')  # Get document vector.
		similarities_dict = self.similarities_to_references(document_triplets_dict) 			# Compute similarities to references.
		self.display_first_k(num_most_similar, similarities_dict) 								# Display suggested languages.

		

# Test
if __name__ == "__main__":
	# Load reference documents dictionary and dictionary for decoding OHCHR language codes.
	references_dicts = np.load('triplets_dicts.npy').item()
	decode_OHCHR = np.load('OHCHR_decode.npy').item()

	# Create new instance of LanguageAnalyzer class.
	la = LanguageAnalyzer(references_dicts, decode_OHCHR)
	la.run(3, 'german.txt')