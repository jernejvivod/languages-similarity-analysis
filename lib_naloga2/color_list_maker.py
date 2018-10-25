import random
import numpy as np
 
 # make_list: make a list of n visually distinguishable RGB values.
 # Scale them to an interval of [0, 1].
def make_list(n):
	res = []
	r = int(random.random() * 256)
	g = int(random.random() * 256)
	b = int(random.random() * 256)
	step = 256 / n  # Define a step in values to make colors distinguishable.
	# Compute RGB values and add to list.
	for i in range(n):
		# Add step.
		r += step
		g += step
		b += step
		# Make sure it is on [0, 255].
		r = int(r) % 256
		g = int(g) % 256
		b = int(b) % 256
		# Scale RGB value to [0, 1] interval and append to list.
		res.append(np.divide((r,g,b), 255)) 
	return res