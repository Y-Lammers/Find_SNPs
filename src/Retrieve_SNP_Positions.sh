#!/bin/bash

# Script arguments: [reference] [output_dir] [sample1.bam] [sample2.bam]

# get and set variables
reference=$1
output_directory=${2%*/}/
sample1=$3
sample2=$4
vcf1=$output_directory$(echo ${sample1%.*} | sed 's/.*\///g')".vcf"
vcf2=$output_directory$(echo ${sample2%.*} | sed 's/.*\///g')".vcf"
DIR=$( cd "$( dirname "$0" )" && pwd )/

# Call SNPs for both samples
${DIR}Call_SNP.sh $reference $output_directory $sample1 &
${DIR}Call_SNP.sh $reference $output_directory $sample2 &
wait

# Remove duplicate SNP positions
grep "^[^#]" $output_directory"variation.vcf" | cut -f1-2 | sort --unique >> $output_directory"unique_variation.txt"

# Get flanking sequences for each SNP and filter remaining results based on coverage of 
# the flanking regions and presence of other SNPs
${DIR}Get_Region.sh $reference $output_directory $sample1 $sample2 $vcf1 $vcf2
