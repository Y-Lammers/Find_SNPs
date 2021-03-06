#!/bin/bash

# Script arguments: [reference] [output_dir] [bam_file]

# get variables
reference=$1
output_directory=$2
bam=$3
base=$output_directory$(echo ${bam%.*} | sed 's/.*\///g')

# get the variable positions from the bam file, filter based on quality and coverage and write
# the results to a vcf file
$(which samtools) mpileup -uIf $reference -d 10000 $bam | $(which bcftools) view -vg - | \
$(which vcfutils.pl) varFilter -d 10 -a 1 | awk '{if (/^#/ || $2>100 && $6>200 && $10 ~ /1\/1/ && length($5) == 1) print }' > $base".vcf"

# cat the vcf files
cat $base".vcf" >> $output_directory"variation.vcf"
