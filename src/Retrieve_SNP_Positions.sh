#!/bin/bash

# Script arguments: [reference] [output_dir] [sample1.bam] [sample2.bam]

# get and set variables
reference=$1
output_directory=${2%*/}/
sample1=$3
sample2=$4
bases1=$output_directory$(echo ${sample1%".bam"} | sed 's/.*\///g')"_snp_positions.txt"
bases2=$output_directory$(echo ${sample2%".bam"} | sed 's/.*\///g')"_snp_positions.txt"
SNP_output=$output_directory"Usuable_SNPs.tsv"
DIR=$( cd "$( dirname "$0" )" && pwd )/

# Call SNPs for both samples
${DIR}Call_SNP.sh $reference $output_directory $sample1 &
${DIR}Call_SNP.sh $reference $output_directory $sample2 &
wait

# Remove duplicate SNP positions
grep "^[^#]" $output_directory"variation.vcf" | cut -f1-2 | sort --unique >> $output_directory"unique_variation.txt"

# Obtain bases for each SNP position
${DIR}Call_Base.sh $reference $output_directory $sample1 &
${DIR}Call_Base.sh $reference $output_directory $sample2 &
wait

# Call the Parse_Bases python script to produce the viable SNP positions file
${DIR}Parse_Bases.py $bases1 $bases2 $SNP_output

# Get flanking sequences for each SNP and filter remaining results based on coverage of 
# the flanking regions and presence of other SNPs
${DIR}Get_Region.sh $reference $output_directory $sample1 $sample2
