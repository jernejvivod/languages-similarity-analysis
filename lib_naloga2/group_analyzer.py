
########################
# Author: Jernej Vivod #
########################

# display_groups: take a list representing the groups in consecutive runs of the k-medoids algorithm
# and display the results to the console in a readable manner.
def display_groups(groups):
	group_index = 1 			# Start indexing groups from 1.
	for group in groups: 		# Go over groups.
		print('\n############\n# group {0}: #\n############'.format(group_index)) 
		for lang in group: 					# Print languages found in next group.
			print('- {0}'.format(lang))
		group_index +=1 	# Increment group index.