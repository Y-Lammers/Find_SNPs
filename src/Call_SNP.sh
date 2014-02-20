#!/bin/bash

# Script arguments: [reference] [output_dir] [bam_file]

# get variables
reference=$1
output_directory=$2
bam=$3
base=$output_directory$(echo ${bam%.*} | sed 's/.*\///g')

# get variation + filter
$(which samtools) mpileup -uf $reference -E -L 10000 -d 10000 $bam | $(which bcftools) view -bvcg - > $base".bcf"
$(which bcftools) view $base".bcf" | $(which vcfutils.pl) varFilter -w 0 -W 0 -a 1 | awk '{if (/^#/ || $6>60) print }' > $base".vcf"

cat $base".vcf" >> $output_directory"variantion.vcf"
