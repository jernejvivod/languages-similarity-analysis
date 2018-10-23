import numpy as np
from lib_HClustering import HierarchicalClustering
from lib_naloga2 import document_comparator

########################
# Author: Jernej Vivod #
########################

# Load data dictionary that maps document names to their vectors.
data = np.load('triplets_dicts.npy').item()
# Initialize HierarchicalClustering distance.
hc = HierarchicalClustering.HierarchicalClustering(data)

# Run clustering and plot dendrogram.
hc.run()
hc.plot_tree()