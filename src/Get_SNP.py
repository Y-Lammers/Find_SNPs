#!/usr/bin/env python

# Arguments: [temp_file] [scaffold] [pos] [vcf file 1] [vcf file 2]

import sys, re, collections

def process_line(line):

	# get the most frequent base and mean quality score

	# split line
	if 'no coverage' in line[0] or len(line) < 5: return [('N', 0)]	

	# sanitize bases
	line[4] = re.sub(r'[^ACTGactg,.\*]',"",line[4])
	line[4] = re.sub(r'[.,]', line[2],line[4]).upper()
	if line[4] == '': return [('N'), 0]

	# return nested list sorted on most common base
	count = collections.Counter(line[4])
	return count.most_common()


def read_vcf(vcf_list):

	# parse throught both the csv_files and return a dictionary
	# with the variable positions and and list with the coverage for the SNPs

	# create the empty dictionaries, prefilted with eiter lists or dictionaries
	snp_cov_dic, snp_var_dic = collections.defaultdict(list), collections.defaultdict(dict)

	# open both vcf files and parse through each line
	count = 0
	for vcf in vcf_list:
	#	for line in open(file, 'r'):
		# split the line and extract the SNP position
		#if line[0] == '#': continue
		line = line.split('\t')
		position = '-'.join(line[:2])

		# fill both dictionaries with the vcf contents
		snp_var_dic[position][line[4]] = count
		snp_cov_dic[position].append(int(line[7].split('=')[1].split(';')[0]))
		count += 1

	# return the filled dictionaries
	return [snp_cov_dic, snp_var_dic]


def zygosity(count):

	# calculate the ratio between the most abundant allele and minor alleles
	allele1, allele2 = count[0][1], sum([var[1] for var in count[1:]])
	return float(allele1)/(allele1+allele2)


def parse_Region():

	# parse the SNP region and check coverage and SNPs / InDels
	
	# set variables
	seq, zyg, cov, location, position = [], 0, [], [sys.argv[2],sys.argv[3]], 0
	ambigu = {'AC':'M','AG':'R','AT':'W','CG':'S','CT':'Y','GT':'K'}

	#vcf_dic = {sys.argv[4]:0,sys.argv[5]:1}
	
	# parse file
	for base in open(sys.argv[1]):
		base = base.strip().split('\t')

		# get nuc count and check coverage
		count = process_line(base)
		cov.append(int(base[3]))		
		if int(base[3]) == 0: break	

		# check zygosity and add reference base to sequence
		if position == 75:
			# if it is the SNP position check if the base is hetrozygous or break
			if zygosity(count) > 0.85 or sum([var[1] for var in count[1:]]) < 10: break
		
			# substract the primary SNP coverage and check if the lesser variant is
			# homozygous, else break
			snp_cov_dic, snp_var_dic = read_vcf([vcf for vcf in vcf_dic])
			count[0] = list(count[0])
			count[0][1] -= sorted(snp_cov_dic['-'.join(location)], reverse=True)[0]
			if zygosity(count) > 0.25: break
			else:
				zyg += 1
				seq.append(ambigu[''.join(sorted([count[0][0],count[1][0]]))])
		else:
			# check zygosity for non SNP bases
			if zygosity(count) <= 0.85:
				zyg += 1
				seq.append(ambigu[''.join(sorted([count[0][0],count[1][0]]))])
			else: seq.append(base[2])

		position += 1

	# check for coverage and zygosity, print the sequence
	# if thresholds are met
	if min(cov) >= 15 and zyg <= 3 and len(seq) == 151:
		SNP = (SNP for SNP,ambi in ambigu.items() if ambi==seq[75]).next()

		# go through the detected alleles and check which allele belongs to which sample
		var_per_sample, spare =  ['',''], ''
		for i in SNP:
			if i in snp_var_dic['-'.join(location)]:
				var_per_sample[snp_var_dic['-'.join(location)][i]] = i
			else: spare += i
		# if there are spare alleles, fill the empty sample with that allele
		if len(spare) == 1:
			var_per_sample = [spare if var == '' else var for var in var_per_sample]

		# reformat the allele and print the location, SNP string and variants to the commandline
		seq[75] = '[{0}/{1}]'.format(SNP[0],SNP[1])
		print '\t'.join(location + [''.join(seq)] + var_per_sample)

# run the script
parse_Region()
