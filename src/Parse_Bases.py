#!/usr/bin/env python

# Arguments: [SNP_file_1] [SNP_file_2] [Usuable_SNP.tsv]

import sys, re, collections

def process_line(line):

	# get the most frequent base and mean quality score

	# split line
	line = line.strip().split('\t')
	if 'no coverage' in line[0] or len(line) < 5: return [('N', 0)]	

	# sanitize bases
	line[4] = re.sub(r'[^ACTGactg,.\*]',"",line[4])
	line[4] = re.sub(r'[.,]', line[2],line[4]).upper()
	if line[4] == '' or int(line[1]) < 76: return [('N'), 0]

	# return nested list sorted on most common base
	count = collections.Counter(line[4])
	return count.most_common()


def get_line(path):

	# return a line
	for line in open(path):
		yield line

def homozygous(count):

	# calculate the ratio between the most abundant allele and minor alleles
	allele1, allele2 = count[0][1], sum([var[1] for var in count[1:]])
	return float(allele1)/(allele1+allele2)


def compare_bases(count1, count2):

	# compare the bases between two groups

	# check that both groups have coverage
	if count1[0][0] in '*N' or count2[0][0] in '*N': return False
	if count1[0][1] < 10 or count2[0][1] < 10: return False
	
	# check if both SNPs are homozygous
	if homozygous(count1) <= 0.85 or homozygous(count2) <= 0.85: return False
	
	# check if positions differ
	if count1[0][0] != count2[0][0]: return True
	else: return False


def parse_files():

	# open the Usuable_SNP.tsv file
	Usuable = open(sys.argv[3], 'w')

	# go through the files and check if the SNP is valid
	gen_2 = get_line(sys.argv[2])
	for line1 in get_line(sys.argv[1]):
		line2 = next(gen_2)

		# count the bases
		count1, count2 = process_line(line1), process_line(line2)

		# compare the position between the groups
		comparison = compare_bases(count1, count2)

		# if the groups differ, write the results to the output file
		if comparison == True:
			cov1, cov2 = str(sum([i[1] for i in count1])), str(sum([i[1] for i in count2]))
			line = line1.strip().split('\t')
			Usuable.write('\t'.join([line[0], line[1], count1[0][0], str(count1[0][1]), cov1, count2[0][0], str(count2[0][1]), cov2, '\n']))
	
	# close the output file
	Usuable.close()

# run the script
parse_files()
