#! /usr/bin/env python
#script to use biopython's blastxml parser to create fasta files for alignment

import sys, csv, Bio, string
from Bio.Blast import NCBIXML

blastfile = sys.argv[1]
# number above which to discard results
e_thresh = 1e-3

#function to reverse complement alignments that are on the opposite strand in the two species
def reverse_complement(hit):
        tbl = string.maketrans('ATGC', 'TACG')
        complement= hit.translate(tbl)[::-1]
        return complement

#function describing output from the blast record
def print_record(align):
	divergence = round(1-(float(align[0].hsps[0].identities)/float(len(align[0].hsps[0].query))), 3)
	title = align[0].title.split(":")[0].lstrip("lcl|").rstrip("\sdna")
	subject = str(align[0].hsps[0].sbjct)
	print "%r\t%r\t%r\n" % (record.query, align[0].hsps[0].query_start, align[0].hsps[0].query_end)
	if align[0].hsps[0].query_start > align[0].hsps[0].query_end:
		subject= reverse_complement(subject)
	#print record.query+"\t"+title+"\t"+str(align[0].hsps[0].sbjct_start)+"\t"+str(align[0].hsps[0].sbjct_end)+"\t"+"\t"+str(align[0].hsps[0].identities)+"\t"+str(len(align[0].hsps[0].query))+"\t"+str(divergence)+"\t"+subject

#code to check for multiple alignments and multiple hits to the same chromosome       
def best_hit(align):
	if len(align[0].hsps) == 1 or align[0].hsps[0].expect != align[0].hsps[1].expect: #check if a best hit exists for the top alignment	
		hit_length = align[0].hsps[0].sbjct_end - align[0].hsps[0].sbjct_start + 1
		if hit_length >= (0.9 * record.query_letters): #only print hits that cover at least 90% of the query sequence
			print_record(align)


#code to run through file of blast records
if blastfile.endswith('.xml'):
   for record in NCBIXML.parse(open(blastfile)):
       align = record.alignments
       if align[0].hsps[0].expect < e_thresh: #check that there is a decent top hit
          if len(align) > 1: #if there are hits to multiple chromosomes
             if align[0].hsps[0].expect != align[1].hsps[0].expect: #check that a best hit exists 
                best_hit(align)	
	     else: #if there is only one alignment, check that a best hit exists
                   best_hit(align)
else:
    print "input not an xml file"
