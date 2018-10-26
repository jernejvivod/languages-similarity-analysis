import numpy as np
from matplotlib import pyplot as plt
from lib_naloga2 import clustering
from lib_naloga2 import group_analyzer
from lib_naloga2 import color_list_maker

########################
# Author: Jernej Vivod #
########################

# Second Home Assignment for the Introduction to Data Analysis Class
# See instructions in folder.
#
# Perform k-medoid clustering on vectors obtained from text documents.

# Load dictionary stored in results_dict.npy that was generated by the text_analyzer script.
results_dict = np.load('triplets_dicts.npy').item()

# Create new instance of KMclustering class implementing methods used for permorming the
# k-medoids clustering algorithm. Initialize with results_dict data.
km = clustering.KMclustering(results_dict)

# Define list that will store the groups found in every run of the k-medoids algorithm.
# Results of each run are represented as a list of list where each sublist represents a group.
groups_by_iteration = []
cluster_silhouettes_by_iteration = []

# Set number of groups and number of iterations for the k-medoids algorithm (Prompt user).
while True:
	num_iterations_in = input('Enter number of iterations of the k-medoids algorithm to compute: ')
	if num_iterations_in.isnumeric():
		NUM_ITERATIONS = int(num_iterations_in)
		break

while True:
	num_groups_in = input('Enter number of groups to use: ')
	if num_groups_in.isnumeric():
		NUM_GROUPS = int(num_groups_in)
		break;

# Make a list of random visually distinguishable RGB values for use with silhouette plots.
silhouette_colors = color_list_maker.make_list(NUM_GROUPS)

print('Performing {0} iterations of k-medoids algorithm on {1} documents...'.format(NUM_ITERATIONS, len(results_dict.keys())))

# Run k medoids algorithm
for k in range(NUM_ITERATIONS):
	print('Computing iteration {0}...'.format(k+1))
	# Run k-medoids algorithm.
	km.run(NUM_GROUPS)
	# Plot iteration silhouette plot.
	km.plot_silhouettes(silhouette_colors)
	plt.title('Silhouette Plot for {0}. Iteration'.format(k+1))
	plt.pause(0.02)
	# Create groups from resulting associations.
	groups = dict((key, [key]) for key in km.associations.values()) 	# Make sure to add medoid to group.
	for assoc in km.associations.keys():
		groups[km.associations[assoc]].append(assoc) 					# Add node associated with medoid to group.

	groups_by_iteration.append([group for group in groups.values()]) 	# Add groups to list of groups by run.
	cluster_silhouettes_by_iteration.append(km.clustering_silhouette) 	# Append cluster silhouette to list of cluster silhouettes by run.


# Display groups formed in every iteration.
iteration_index = 1
for iteration_groups in groups_by_iteration:
	print("\n**************************** Groups in iteration {0} ****************************".format(iteration_index))
	group_analyzer.display_groups(iteration_groups)
	iteration_index += 1
plt.show()

# Display cluster silhouette values by iteration.
s = plt.bar(list(range(1, len(cluster_silhouettes_by_iteration) + 1)), cluster_silhouettes_by_iteration, color = 'skyblue')
plt.xlabel('Iteration index')
plt.ylabel('Clustering silhouette value')
plt.title('Clustering Silhouette Value by Iteration')
plt.show()