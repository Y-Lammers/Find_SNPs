#!/bin/bash

# Script arguments: [reference] [output_dir] [sample1.bam] [sample2.bam]

# get and set variables
reference_file=$1
output_directory=${2%*/}/
sample1=$3
sample2=$4
bases1 = $output_directory$(echo ${sample1%".bam"} | sed 's/.*\///g')"_snp_positions.txt"
bases2 = $output_directory$(echo ${sample2%".bam"} | sed 's/.*\///g')"_snp_positions.txt"
SNP_output = $output_directory"Usuable_SNPs.tsv"

# Call SNPs for both samples
Call_SNP.sh $reference $output_directory $sample1
Call_SNP.sh $reference $output_directory $sample2

# Remove duplicate SNP positions
grep "^[^#]" $output_directory"variantion.vcf" | cut -f1-5 | sort --unique >> $output_directory"unique_variation.txt"

# Obtain bases for each SNP position
Call_Base.sh $reference $output_directory $sample1
Call_Base.sh $reference $output_directory $sample2

# Call the Parse_Bases python script to produce the viable SNP positions file
Parse_Bases.py $bases1 $bases2 $SNP_output
