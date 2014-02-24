#!/usr/bin/env python

# Arguments: [temp_file] [Usuable_SNP] [scaffold] [pos]

import sys, re, collections

def read_Usuable():

	# Open the Usuable dic file and return a dictionary with
	# the SNP alleles for both populations

	Usuable_dic = {}
	for SNP in open(sys.argv[2]):
		SNP.strip().split('\t')
		Usuable_dic['-'.join(SNP[0:2])] = [SNP[2], SNP[5]]
	
	# return the dictionary
	return Usuable_dic


def process_line(line):

	# get the most frequent base and mean quality score

	# split line
	line = line.strip().split('\t')
	if 'no coverage' in line[0] or len(line) < 5: return [('N', 0)]	

	# sanitize bases
	line[4] = re.sub(r'[^ACTGactg,.\*]',"",line[4])
	line[4] = re.sub(r'[.,]', line[2],line[4]).upper()
	if line[4] == '': return [('N'), 0]

	# return nested list sorted on most common base
	count = collections.Counter(line[4])
	return count.most_common()


def zygosity(count):

	# calculate the ratio between the most abundant allele and minor alleles
	allele1, allele2 = count[0][1], sum([var[1] for var in count[1:]])
	return float(allele1)/(allele1+allele2)


def parse_Region(Usuable_dic):

	# parse the SNP region and check coverage and SNPs / InDels
	
	# set variables
	seq, zyg, cov, location = '', 0, [], [sys.argv[2],sys.argv[3]]
	
	# parse file
	for base in open(sys.argv[1]):
		base = base.strip().split('\t')

		# add reference base to sequence
		seq += base[2]

		# get nuc count
		count = process_line(base)

		# check zygosity
		if zygosity(count) <= 0.85: zyg += 1

		# add coverage to coverage list
		cov.append(int(base[3]))

	# check for coverage and zygosity, print the sequence
	# if thresholds are met
	if min(cov) >= 10 and zygosity <= 3:
		sequence[75] = '[{0}/{1}]'.format(*tuple(Usuable_dic['-'.join(location)]))
		print '\t'.join(location + [sequence, '\n'])


# run the script
parse_Region(read_Usuable())
