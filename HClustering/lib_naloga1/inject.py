########################
# Author: Jernej Vivod #
########################

# inject_distances: append distances from two nested clusters constituting a higher order cluster.
# The results of this functions are used to make a dendrogram plot that is proportional to the distances between the clusters.
# The distances list maps clusters to distances between their nested clusters.
def inject_distances(clusters, distances):
	for clust_d in distances:								# Go over every cluster in distances and inject distance to corresponding cluster.
		inject(clust_d[0], clust_d[1], clusters)
	clusters.insert(0, distances[len(distances) - 1][1]) 	# The last cluster is the list of clusters itself. Handle individually (inject last distance in distances list).

# inject: auxiliary recursive function that finds the cluster in the original clusters list and append distance to the front.
def inject(cluster, distance, clusters):
	for index, c in enumerate(clusters):					# Go over every cluster in clusters at current place.
		if c == cluster: 									# If found cluster, inject distance.
			clusters[index] = [distance] + clusters[index]
		elif isinstance(c, list): 							# Else if element is itself a cluster, make recursive call for subcluster.
			inject(cluster, distance, c)