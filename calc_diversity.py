#note: if cogent not in ~/bin then specify path using sys

from cogent import LoadSeqs, DNA
from cogent.app.clustalw import align_unaligned_seqs as clustalw_align_unaligned_seqs
from cogent.evolve.pairwise_distance import TN93Pair

file = open("alignment_input.txt")
for line in file:
	fields = line.rstrip("\n").split("\t")

#load sequences to Cogent format
	seq_data = {fields[0]:fields[1],
	fields[2]:fields[3],
	fields[4]:fields[5]}
	seqs = LoadSeqs(data = seq_data, moltype=DNA, aligned=False)

#align sequences with clustalw
	aln = clustalw_align_unaligned_seqs(seqs, DNA)

#calculate genetic distances
	dist_calc = TN93Pair(DNA, alignment=aln)
	dist_calc.run()
	dists = dist_calc.getPairwiseDistances()

#parse distance calculations
#turk/finch
	f_dist = abs(dist_calc.Dists[:4,:4][0,2])

#turk/chick
	c_dist= abs(dist_calc.Dists[:4,:4][0,3])

	print 
