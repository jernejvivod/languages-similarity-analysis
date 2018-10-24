import os
import numpy as np
import sys
from lib_naloga2 import document_vectorizator

# This script produces and saves a dictionary that maps each text file name to a dictionary that maps
# each triplet that appears in the text file to its tf-idf value (maps each document to its vector).

########################
# Author: Jernej Vivod #
########################

# Load OHCHR code mapping dictionary.
decode_OHCHR = np.load('./lib_naloga2/OHCHR_decode.npy').item()

# Prompt user whether to convert UDHR translations or news headliens to vectors represented as dictionaries.
while True:
	mode = input('create vectors for Universal declaration of human rights translations or news headlines? (u/n): ')
	# Convert UDHR translations to vectors (represented as dictionaries).
	if mode == 'u':
		while True:
			compute_idf = input('Use inverse document frequencies in vector computations (might be slow for large ammounts of text)? (y/n): ')
			DOCS_PATH = './data/UHDHR_translations/'
			documents = set(os.listdir(DOCS_PATH))
			# Get dictionary where name of document file is mapped to dictionary that maps triplets
			# that appear in it to their tf-idf values.
			if compute_idf == 'y' or compute_idf == 'n':
				results_dict = document_vectorizator.documents_to_vectors(documents, DOCS_PATH, True if compute_idf == 'y' else False)
				for key in list(results_dict.keys()):
					results_dict[decode_OHCHR[key[:-4]]] = results_dict.pop(key)

				# Save resulting dictionary to file.
				np.save('triplets_dicts.npy', results_dict)
				sys.exit(0)
			else:
				pass
			
			
	# for each language, concatenate text from news site headlines into single document and make into vector (represented as a dict).
	elif mode == 'n':
		DOCS_PATH = './data/news_headlines/' 		# path to folder containing the news sites
		languages = list(os.listdir(DOCS_PATH)) 	# List folders containing news headlines for each language.
		for lang in languages: 						# Go over folders for each language.
			news_concat = '' 						# Define an empty string that will be used as base for concatenation.
			DOC_PATH = './data/news_headlines/' + lang + '/'  # path to news headlines in this language.
			documents = list(os.listdir(DOC_PATH)) 			# Make a list of documents containing the headlines in this language.
			for document in documents: 						# Concatenate to base string.
				document_text = open(DOC_PATH + document, encoding="utf8").read()
				news_concat += document_text
				SAVE_PATH = './data/concatenated-news-headlines/' + lang  # Save concatenations to document.
				with open(SAVE_PATH, 'w') as f:
					f.write(news_concat)
		DOCS_PATH = './data/concatenated-news-headlines/'
		documents = set(os.listdir(DOCS_PATH))
		# Get dictionary where name of document file is mapped to dictionary that maps triplets
		# that appear in it to their tf-idf values.
		while True:
			compute_idf = input('Use inverse document frequencies in vector computations (might be slow for large ammounts of text)? (y/n): ')
			if compute_idf == 'y' or compute_idf == 'n':
				results_dict = document_vectorizator.documents_to_vectors(documents, DOCS_PATH, True if compute_idf == 'y' else False)
				# Save resulting dictionary to file.
				np.save('triplets_dicts.npy', results_dict)
				sys.exit(0)
			else:
				pass
	else:
		pass

	