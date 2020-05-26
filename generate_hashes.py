# Generate 1000 spaced hashes for 1000 possible experimental subjects.

# Example
import base64
s = "Nobody inspects the spammish repetition".encode('utf-8')
encoded = base64.urlsafe_b64encode(s)
decoded = base64.urlsafe_b64decode(encoded)
#print('Original:\n',s)
#print('Encoded:\n', encoded)
#print('Decoded:\n', decoded)

# 1- Generate 1000 random strings and their corresponding hashes

import string
from numpy import random
def random_string(stringLength=12):
	letters = string.ascii_lowercase
	return ''.join(random.choice(list(letters)) for i in range(stringLength))

def generate_random_hashes(n_hashes=1000, seed=1):
	random.seed(seed)
	random_strs = [ random_string() for _ in range(n_hashes) ]
	random_hashes = [ base64.urlsafe_b64encode(s.encode('utf-8')) for s in random_strs  ]

	"""
	print('Random strings:')
	for i in random_strs:
		print(i)
	print('\nCorresponding URL-safe base 64hashes:')
	for i in random_hashes:
		print(i)
	"""

	# Save

	with open('random_strings_seed{}.txt'.format(n_hashes),'w') as f:
		f.write('\n'.join(random_strs))

	with open('random_hashes_seed{}.txt'.format(n_hashes),'w') as f:
		f.write('\n'.join([ i.decode('utf-8') for i in random_hashes ]))

	return random_hashes

# 2- Check that those hashes are distant from each other.

# pip install python-Levenshtein 

# Informally, the Levenshtein distance between two words is the minimum number
# of single-character edits (insertions, deletions or substitutions) required
# to change one word into the other. Also known as edit distance.

from Levenshtein import distance as levenshtein_distance
from itertools import combinations
import matplotlib.pyplot as plt

def test_random_hashes(hashes):
	s_hashes = [ i.decode('utf-8') for i in hashes ]
	distances = ( levenshtein_distance(si, sj) for si, sj in combinations(s_hashes,2) )
	distances = list(distances)
	plt.hist(distances, bins=20)
	plt.yscale('log')
	plt.ylabel('Count (total={})'.format(len(distances)))
	plt.xlabel('Distance between pairs of hashes')
	plt.show()

# Conclusion: with 1000 alphanumeric hashes of length 16,
# only two pairs of hashes have an edit distance < 8.
#
# This means that if an user for some reason changes < 7 characters in their hash,
# it will still be a unique hash.
