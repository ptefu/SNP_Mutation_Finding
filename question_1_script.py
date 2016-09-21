from pileup import PileUp
from approximate_matcher import ApproximateMatcher
import sys

# import the fasta files
f = open(sys.argv[1], 'r')
g = open(sys.argv[2], 'r')
reference  = ""
for line in f:
    reference += line.rstrip()
reads = (g.readline()).rstrip().split()

reference.rstrip()
print reference[822:835]
# initialize object
am = ApproximateMatcher(reference)
pileup = PileUp(reference)
d = 3

for read in reads:
	# find matching positions for a given read
	# assumes positions is a list (even if only a single match is found)
	# with matching positions
	positions = am.get_matches(read, d)
	if len(positions) > 0:
		# add to pileup object
		pileup.insert(positions, read)

# prints out mismatching positions
# output is:
# (<position>, <reference_character>, [(<variant_character>,
# <num_times_aligned>)])
# argument filters mismatch by frequency in which variant character
# is observe, e.g., .01 means variant character has to be seen at least
# once for every 100 aligned nucleotides
pileup.print_mismatches(.01)
