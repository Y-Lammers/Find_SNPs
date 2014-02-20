#!/bin/bash

# Script arguments: [reference] [output_dir] [bam]
# get variables
reference_file=$1
output_directory=$2
bam=$3
variation=$output_directory"unique_variation.txt"

# parse through variation file
while read l; do
	# grab the SNP coordinates
	echo $l | while read -r scaf pos stuff; do
		echo $scaf $pos;

		# use mpileup to echo and write the exact coverage
		variation=$(/usr/local/src/samtools-0.1.19/samtools mpileup -r $scaf":"$pos"-"$pos -f $reference_file $bam)
		if [ -z "$variation" ]; then
			variation="no coverage"
		fi
		echo "$variation" >> $output_directory$(echo ${bam%".bam"} | sed 's/.*\///g')"_snp_positions.txt"
	done;
done < $variation
