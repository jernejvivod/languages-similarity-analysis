########################
# Author: Jernej Vivod #
########################

# extract_names: extract all string values in a cluster
def extract_names(cluster):

	# extract_names_gen: Auxiliary generator varaible that flattens a nested list and yields string values.
	def extract_names_gen(cluster):
		for group in cluster:
			if isinstance(group, str):
				yield group
			else:
				yield from extract_names(group)

	return list(extract_names_gen(cluster))