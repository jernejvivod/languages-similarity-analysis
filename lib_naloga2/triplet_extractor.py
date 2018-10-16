import numpy as np
import re

########################
# Author: Jernej Vivod #
########################

# text_to_triplets_dict: convert a string to a dictionary that maps each triplet that appears
# in the text to its relative frequency.
def text_to_triplets_dict(text):
	# multiple_replace: replace elements in list replace with '' (remove them)
	def multiple_replace(text, replace):
		rx = re.compile('|'.join(map(re.escape, replace))) 	# Build regular expression.
		return rx.sub('', text)

	# histc: The function counts the number of elements of X that fall in the histogram bins defined by bins.
	# This is a Python implementation of the MATLAB histc function.
	def histc(x, bins):
		map_to_bins = np.digitize(x, bins) 	# Get indices of the bins to which each value in input array belongs.
		res = np.zeros(bins.shape)
		for el in map_to_bins:
			res[el-1] += 1 					# Increment appropriate bin.
		return res

	# triplets_to_dict: convert numpy matrix where each column represents a triplet to a dictionary that maps
	# each unique triplet to its relative frequency.
	def triplets_to_dict(triplets):
		# Get unique columns, indices of columns in the original matrix and the indices that reconstruct the original
		# matrix.
		u, indices, inverse = np.unique(triplets, axis=1, return_index=True, return_inverse=True)
		# Compute number of occurences of each triplet in the matrix.
		num_triplets = histc(inverse, np.array(range(max(inverse) + 1)))
		probabilities = np.true_divide(num_triplets, sum(num_triplets)) 		# Get probabilities.

		# Build dictionary.
		res_dict = dict()
		for i in range(u.shape[1]):
			res_dict[''.join(u[:,i])] = probabilities[i]

		print("sum = {0}".format(sum(res_dict.values())))
		return res_dict

	# Define list of delimiters to be removed from text.
	replace = [",", ".", "!", "?", "/", "&", "-", ":", ";", "@", "'", "...", '\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
	text = multiple_replace(text, replace).lower() 	# Remove delimiters.
	fst = np.array(list(text)) 					 	# Convert to char array.
	snd = np.roll(fst, -1) 							# roll (circshift) to obtain triplets.
	thd = np.roll(fst, -2)
	triplets = np.stack((fst, snd, thd)) 			# Stack to 2xn matrix.
	triplets = triplets[:, :-2] 					# Remove triplets introduced by roll.
	return triplets_to_dict(triplets)

