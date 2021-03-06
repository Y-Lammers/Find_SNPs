#!/bin/bash

# Script arguments: [reference] [output_directory] [bam1] [bam2] [vcf1] [vcf2]
# get variables
reference_file=$1
output_directory=$2
bam1=$3
bam2=$4
vcf1=$5
vcf2=$6
SNPs=$output_directory"SNP_file.csv"
merged=$output_directory"merged.bam"
Usuable=$output_directory"unique_variation.txt"
DIR=$( cd "$( dirname "$0" )" && pwd )/

# merge the two bam files
$(which samtools) merge $merged $bam1 $bam2

# index the bam file
$(which samtools) index $merged

# write the header to the SNP file
echo -e "#Contig\tPosition\tSequence\t"$vcf1"\t"$vcf2 > $SNPs

# parse through Usuable_SNP file
while read l; do
	# grab the SNP coordinates
	echo $l | while read -r scaf pos stuff; do
		pos1=$(($pos-100))
		pos2=$(($pos+100))
		echo $scaf $pos $pos1 $pos2;

		# use mpileup to echo and write the exact coverage
		variation=$($(which samtools) mpileup -r $scaf":"$pos1"-"$pos2 -f $reference_file $merged)

		sub_vcf1=$(grep -P "$scaf\t$pos" $vcf1)
		sub_vcf2=$(grep -P "$scaf\t$pos" $vcf2)

		# write the variation and get the sequence with the Select_SNP.py script
		echo "$variation" > $output_directory"temp.tsv"
		${DIR}Get_SNP.py $output_directory"temp.tsv" $scaf $pos "$sub_vcf1" "$sub_vcf2" >> $SNPs
	done;
done < $Usuable
rm $output_directory"temp.tsv"
