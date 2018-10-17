def decode_names(groups, decode_dict):
	for iteration in range(len(groups)):
		for group_index in range(len(groups[iteration])):
			groups[iteration][group_index] = [decode_dict[code[:-4]] for code in groups[iteration][group_index]]
		return groups

def display_groups(groups):
	group_index = 1
	for group in groups:
		print('\n############\n# group {0}: #\n############'.format(group_index))
		for lang in group:
			print('- {0}'.format(lang))
		group_index +=1