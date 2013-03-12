#! /usr/bin/env python
from sys import argv
import re

script, input = argv

f = open(input)
cluster= []
for line in f:
#get clusters to analyse
	if line.startswith('>'):
		if len(cluster) == 4 and species == 3:
			for i in cluster:
				print i
		clust_size = 0
		cluster[:] = []
		chick = 0
		turk = 0
		finch = 0
		species = 0
		cluster.append(line)
	else:
		clust_size = clust_size + 1
		if 'ENSGALG' in line:
			chick = 1
		elif 'ENSMGAG' in line:
			turk = 1
		elif 'ENSTGUG' in line:
			finch = 1
		species = chick + turk + finch 
		cluster.append(line)

	

	

