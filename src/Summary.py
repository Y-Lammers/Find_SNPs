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

		vcf_dic['-'.join(line[:1])] = line[4]

	return vcf_dic		


def print_summary():

	# read the VCF files
	#vcf1 = Read_VCF(sys.argv[2])
	#vcf2 = Read_VCF(sys.argv[3])

	vcf = [Read_VCF(sys.argv[2]), Read_VCF(sys.argv[3])]

	# parse through the SNP file
	for line in open(sys.argv[1], 'r'):
		line = line.split('\t')

		# get the variant in the SNP file
		var = line[2].split('/')
		var = [var[0][-1], var[1][0]]

		#host1, host2 = '', ''
		hosts = ['','']

		for i in range(0,2):
			try:
				hosts[i] = vcf[i]['-'.join(line[:1])]
				var = [nuc for nuc in var if nuc != hosts[i]]
			except:
				pass

		for i in range(0,2):
			if hosts[i] == '':
				hosts[i] == var.pop(0)
		
		if len(var) > 0:
			#print 'error '*3
			print line
			#print var

print_summary()
