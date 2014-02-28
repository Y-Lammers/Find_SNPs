#!/usr/bin/env python

# imput is: [gff3] [SNP file]

import sys

def parse_gff3():

	# Parse the gff3 annotation file and extract the genes
	# + mrna, exon and CDS information. 

	# create dictionary and open gff3 file
	annon_dic, gff3_file = {}, open(sys.argv[1])

	# parse through the gff3 file and extract the info for each gene
	for gff3 in gff3_file:

		# get gene information
		gff3 = gff3.strip().split('\t')
	
		# add the gene information to the dictionary
		annon_dic[gff3[0]] = annon_dic.get(gff3[0],[]) + [gff3]

	# return the dictionary with the annotations
	return annon_dic

def parse_SNP(annon_dic):

	# get the location for each SNP and check if these
	# are located in a gene

	# parse the SNP file
	for SNP in open(sys.argv[2]):
		SNP = SNP.strip().split('\t')

		# check if SNP is located in an annotated region
		for annon in annon_dic[SNP[0]]:

			# get the location in bases for the annotation
			start, stop = annon[3:5]

			# check if the SNP location is between the start - stop of the feature
			if int(SNP[1]) >= int(start) and int(SNP[1]) <= int(stop):
			
				# if the SNP is located between in a annotation, print the
				# SNP + annotation to the stdout
				print '{0}\t{1}'.format('\t'.join(SNP),'\t'.join(annon))

# parse the SNP file
parse_SNP(parse_gff3())
	


