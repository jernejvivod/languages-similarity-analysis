import math

########################
# Author: Jernej Vivod #
########################

# euclidean_dist: compute similarity between samples sample_1 and sample_2 by means of their euclidean distance.
def euclidean_dist(sample_1, sample_2):
	# Sum squares of differences.
	sum_squares = 0
	for i in range(len(sample_1)):
		sum_squares += (sample_1[i] - sample_2[i])**2;

	# Take square root of sum.
	sum_squares = math.sqrt(sum_squares)

	return sum_squares

# manhattan_dist: compute similarity between samples sample_1 and sample_2 by means of their manhattan distance.
def manhattan_dist(sample_1, sample_2):
	sum_abs = 0
	for i in range(len(sample_1)):
		sum_abs += abs(sample_1[i] - sample_2[i])

	return sum_abs