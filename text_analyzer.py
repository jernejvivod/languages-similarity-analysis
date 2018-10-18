import os
import numpy as np
from lib_naloga2 import document_vectorizator

# This script produces and saves a dictionary that maps each text file name to a dictionary that maps
# each triplet that appears in the text file to its tf-idf value.

########################
# Author: Jernej Vivod #
########################

# Prompt user whether to convert UDHR translations or news headliens to vectors represented as dictionaries.
while True:
	mode = input('create vectors for Universal declaration of human rights translations or news headlines? (u/n): ')
	# Convert UDHR translations to vectors (represented as dictionaries).
	if mode == 'u':
		DOCS_PATH = './data/translations/'
		documents = set(os.listdir(DOCS_PATH))
		# Get dictionary where name of document file is mapped to dictionary that maps triplets
		# that appear in it to their tf-idf values.
		results_dict = document_vectorizator.documents_to_vectors(documents, DOCS_PATH)

		# Save resulting dictionary to file.
		np.save('triplets_dicts.npy', results_dict)
		break;
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
				SAVE_PATH = './data/news_headlines/concatenated/' + lang  # Save concatenations to document.
				with open(SAVE_PATH, 'w') as f:
					f.write(news_concat)
		DOCS_PATH = './data/news_headlines/concatenated/'
		documents = set(os.listdir(DOCS_PATH))
		# Get dictionary where name of document file is mapped to dictionary that maps triplets
		# that appear in it to their tf-idf values.
		results_dict = document_vectorizator.documents_to_vectors(documents, DOCS_PATH)
		
		# Save resulting dictionary to file.
		np.save('triplets_dicts.npy', results_dict)
		break;
	else:
		pass

	