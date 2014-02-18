#!/bin/bash

# Script arguments: [reference] [output_dir] [bam_file]

# get variables
reference_file=$1
output_directory=$2
bam=$3
base=$output_directory${bam%.*}

# get variation + filter
samtools mpileup -uf $reference_file -E -L 10000 -d 10000 $bam | bcftools view -bvcg - > $base".bcf"
bcftools view $base".bcf" | /usr/share/samtools/vcfutils.pl varFilter -w 0 -W 0 -a 1 | awk '{if (/^#/ || $6>60) print }' > $base".vcf"

cat $base".vcf" >> $output_directory"variantion.vcf"
