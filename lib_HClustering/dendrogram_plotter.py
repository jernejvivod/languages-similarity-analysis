# plot_dendogram_ascii: plot an ascii graphical representation of a dendogram represented as a list where
# a node contains the distance between the subtrees and the subtrees and a leaf contains a string representing the base sample.
# The function is based on a binary tree plotting function but modified to print stem lengths proportional to distances between clusters.

########################
# Author: Jernej Vivod #
########################

def plot_dendrogram_ascii(D):
    
    # is_node: check if List represents a node (contains nested lists).
    def is_node(D):
        return isinstance(D, list) and len(D) == 3
    
    # max_height: return the highest subtree.
    # If subtree is a leaf, return length of string representing a leaf in tree.
    def max_height(D):
        if is_node(D):
            height = max(max_height(D[1]), max_height(D[2]))
        else:
            height = len(str(D))
        return height
        
    # Create an empty list for storing heights of levels in dendrogram.
    levels = []

    # traverse: plot dendrogram represented by D
    def traverse(D, height, is_first, dist):
        # If D is a node:
        if is_node(D):
            traverse(D[1], height, 1, D[0])   # Draverse for left subtree.
            s = [' ']*(height + D[0])         # Add spaces - proportional to cluster difference.
            s.append('|')
        # Else if D is a leaf (contains string representing the country's name)
        else:
            s = list(str(D))         # convert leaf string to list of characters for manipulation.
            s.append(' ')               # Add space after leaf string (char list).

        while len(s) < height + dist:        # While length of leaf character list has not reached the specified height...
            s.append('=')               # ...elongate stem.
        
                                        # If is_first >= 0:
        if is_first >= 0:
            s.append('+')               # Add elbow.
            if is_first:                # If is_first > 0...
                levels.append(height + dist)
            else:
                levels.remove(height + dist)

        # Sort levels in ascending order.
        levels.sort()
        for level in levels:                    # Go over levels
            if len(s) < level:                  # If the length of row is smaller than the next level height...
                while len(s) < level:           # Fill row with one less spaces than the level height.
                    s.append(' ')
                s.append('|')                   # Close with |.

        print(''.join(s))                       # Join character lists into string and print.
        
        if is_node(D):                          # If D is a node, traverse right subtree.
            traverse(D[2], height, 0, D[0])

    # call traverse with initial values for parameters.
    traverse(D, max_height(D), -1, 5)