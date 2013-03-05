#note: if cogent not in ~/bin then specify path using sys
#note: this script accepts a file of sequences for alignment in the format name\tsequence\t etc.
#note: this is a quick and dirty script written in a hurry, which I intend to come back and generalise.

from sys import argv
from cogent import LoadSeqs, DNA
from cogent.app.clustalw import align_unaligned_seqs as clustalw_align_unaligned_seqs
from cogent.evolve.pairwise_distance import TN93Pair

#bit to get number of species - not needed currently, unless sequence loading is generalised to accept an unspecified number of species.
script, num_species = argv


file = open("alignment_input.txt")
for line in file:
	fields = line.rstrip("\n").split("\t")

#load sequences to a cogent sequence object, moltype DNA
	seq_data = {fields[0]:fields[1],
	fields[2]:fields[3],
	fields[4]:fields[5]}
	seqs = LoadSeqs(data = seq_data, moltype=DNA, aligned=False)

#align sequences with clustalw (must be installed and in path)
	aln = clustalw_align_unaligned_seqs(seqs, DNA)

#calculate genetic distances
	dist_calc = TN93Pair(DNA, alignment=aln)
	dist_calc.run()
	dists = dist_calc.getPairwiseDistances()

#parse distance calculations
#turk/finch
	f_dist = round(abs(dist_calc.Dists[:4,:4][0,2]),3)

#turk/chick
	c_dist= round(abs(dist_calc.Dists[:4,:4][0,3]),3)

	print "turk_finch\t%d\tturk_chick\t%d" % (f_dist, c_dist) 
