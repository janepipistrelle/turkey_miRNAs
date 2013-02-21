#! /usr/bin/env python
#script to use biopython's blastxml parser to create fasta files for alignment

import sys, csv, Bio
from Bio.Blast import NCBIXML

blastfile = sys.argv[1]
# number above which to discard results
e_thresh = 1e-3

#function describing output from the blast record
def print_record(align):
       divergence = round(1-(float(align[0].hsps[0].identities)/float(len(align[0].hsps[0].query))), 3)
       print record.query+"\t"+str(align[0].title[4:6]).rstrip()+"\t"+str(align[0].hsps[0].sbjct_start)+"\t"+str(align[0].hsps[0].sbjct_end)+"\t"+"\t"+str(align[0].hsps[0].identities)+"\t"+str(len(align[0].hsps[0].query))+"\t"+str(divergence)+"\t"+align[0].hsps[0].sbjct
       
#code to check for multiple alignments and multiple hits to the same chromosome
if blastfile.endswith('.xml'):
   for record in NCBIXML.parse(open(blastfile)):
       align = record.alignments
       if align[0].hsps[0].expect < e_thresh: #check that there is a decent top hit
          if len(align) > 1: #if there are hits to multiple chromosomes
             if align[0].hsps[0].expect != align[1].hsps[0].expect: #check that a best hit exists 
                if len(align[0].hsps) ==1 or align[0].hsps[0].expect != align[0].hsps[1].expect: #if a best hit exists on the top alignment then print
                   print_record(align)
          else: #if there is only one alignment, check for multiple hits to that chromosome
                if len(align[0].hsps) == 1 or align[0].hsps[0].expect != align[0].hsps[1].expect: #if a best hit exists then print
                   print_record(align)
else:
    print "input not an xml file"
