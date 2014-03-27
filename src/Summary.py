#!/usr/bin/env python

# arugments [SNP file] [vcf file 1] [vcf file 2]

import sys

def Read_VCF(vcf_file):

	# set dictionary
	vcf_dic = {}

	# open the file and parse through the SNPs
	for line in open(vcf_file, 'r'):
		if line[0] == '#': continue
		line = line.split('\t')

		# fill the vcf dictionary
		vcf_dic['-'.join(line[:2])] = line[4]

	# return the dictionary
	return vcf_dic		


def print_summary():

	# read the VCF files
	vcf = [Read_VCF(sys.argv[2]), Read_VCF(sys.argv[3])]

	print 'contig\tposition\t{0}\t{1}'.format(sys.argv[2],sys.argv[3])

	# parse through the SNP file
	for line in open(sys.argv[1], 'r'):
		line = line.split('\t')

		# get the variant in the SNP file
		var = line[2].split('/')
		var = [var[0][-1], var[1][0]]
		hosts = ['','']

		# try to obtain the SNP for each sample
		for i in range(0,2):
			try:
				hosts[i] = vcf[i]['-'.join(line[:2])]
				var = [nuc for nuc in var if nuc != hosts[i]]
			except:
				pass

		# if a host has no SNP in the vcf file, replace it with the consensus
		# from the SNP file
		for i in range(0,2):
			if hosts[i] == '': hosts[i] == var.pop(0)
		
		# print the results if all alleles have been consumed
		if len(var) == 0:
			print '{0}\t{1}\t{2}\t{3}'.format(line[0], line[1], hosts[0], hosts[1])

print_summary()
