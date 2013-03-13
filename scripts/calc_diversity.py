#note: if cogent not in ~/bin then specify path using sys
#note: this script accepts a file of sequences for alignment in the format name\tsequence\t etc.
#note: this is a quick and dirty script written in a hurry, which I intend to come back and generalise.

from sys import argv
from cogent import LoadSeqs, DNA
from cogent.app.clustalw import align_unaligned_seqs as clustalw_align_unaligned_seqs
from cogent.evolve.pairwise_distance import TN93Pair

#bit to get number of species - not needed currently, unless sequence loading is generalised to accept an unspecified number of species.
script, infile, outfile, num_species = argv


file = open(infile)
out = open(outfile, 'w')

#specific for this job
out.write("locus\tturk/chick\tturk/finch\n")

#get sequence names
def get_sequence_names(line):
        	fields = line.rstrip("\n").split("\t")
		names = []
		for i in range(len(fields)):
			if i % 2 == 0:
				names.append(fields[i])
		return names

def make_seq_object(line):
	fields = line.rstrip("\n").split("\t")
	seq_data = {}
	for i in range(len(fields)):
                        if i % 2 == 0:
                                seq_data[fields[i]] = fields[i+1]
	seqs = LoadSeqs(data = seq_data, moltype=DNA, aligned=False)        
        return seqs

for line in file:
	names = get_sequence_names(line)
	seqs = make_seq_object(line)

#align sequences with clustalw (must be installed and in path)
	aln = clustalw_align_unaligned_seqs(seqs, DNA)

#calculate genetic distances
	dist_calc = TN93Pair(DNA, alignment=aln)
	dist_calc.run()
	dists = dist_calc.getPairwiseDistances()

#parse distance calculations
	sp_1_2 = round(abs(float(dists[names[0], names[1]])),3)
	sp_2_3 = round(abs(float(dists[names[0], names[2]])),3)
	out_line = "%s\t%r\t%r\n" % (names[0], sp_1_2, sp_2_3)
	out.write(out_line)

file.close()
out.close()
