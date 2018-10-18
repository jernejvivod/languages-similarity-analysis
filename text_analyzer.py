import os
import numpy as np
from lib_naloga2 import document_vectorizator

# This script produces and saves a dictionary that maps each text file name to a dictionary that maps
# each triplet that appears in the text file to its tf-idf value.

########################
# Author: Jernej Vivod #
########################

# Parse text files from folder.
DOCS_PATH = './data/translations/'
documents = set(os.listdir(DOCS_PATH))

# Get dictionary where name of document file is mapped to dictionary that maps triplets
# that appear in it to their tf-idf values.
results_dict = document_vectorizator.documents_to_vectors(documents, DOCS_PATH)

# Save resulting dictionary to file.
np.save('triplets_dicts.npy', results_dict)