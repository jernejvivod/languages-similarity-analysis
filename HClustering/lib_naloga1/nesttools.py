########################
# Author: Jernej Vivod #
########################

# un_nest: extract all integers contained in list l that may contain nested lists of integers.
def un_nest(l):
	for el in l: 						# Go over elements in list.
		if isinstance(el, str): 		# If element is an integer, yield.
			yield el
		elif isinstance(el, list): 		# Else if element is a nested list, yield from recursive call results.
			yield from un_nest(el)