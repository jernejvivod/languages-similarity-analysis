import os
import numpy as np
from lib_naloga2 import document_vectorizator

# This script produces and saves a dictionary that maps each text file name to a dictionary that maps
# each triplet that appears in the text file to its tf-idf value.

########################
# Author: Jernej Vivod #
########################

# Parse text files from folder.
documents = set(os.listdir('./data/translations'))

# Get dictionary where name of document file is mapped to dictionary that maps triplets
# that appear in it to their tf-idf values.
results_dict = document_vectorizator.documents_to_vectors(documents)

# Save resulting dictionary to file.
np.save('results_dict.npy', results_dict)