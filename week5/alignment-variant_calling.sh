#!/bin/bash

index the reference genome for alignment using bwa
bwa index sacCer3.fa

align sequencing data to the reference genome using bwa
for sample in *.fastq
	do
		echo "Aligning sample:" ${sample}
		bwa mem -t 4 -R "@RG\tID:${sample}\tSM:${sample}" sacCer3.fa \
			${sample} > ${sample}.sam
	done

sort aligned files, convert to bam, and index using samtools
for sample in *.fastq.sam
	do
		# sorting each aligned fastq.sam file and saving the output as .bam with a "sorted_" prefix
		samtools sort -O bam -o sorted_${sample%.sam}.bam ${sample}
		# indexing each aligned, sorted .bam file
		samtools index sorted_${sample%.sam}.bam
	done

index the reference genome using samtools
samtools faidx sacCer3.fa

call variants using samtool sequencing data
freebayes -f sacCer3.fa \
	--bam sorted_A01_09.fastq.bam \
	--bam sorted_A01_11.fastq.bam \
	--bam sorted_A01_23.fastq.bam \
	--bam sorted_A01_24.fastq.bam \
	--bam sorted_A01_27.fastq.bam \
	--bam sorted_A01_31.fastq.bam \
	--bam sorted_A01_35.fastq.bam \
	--bam sorted_A01_39.fastq.bam \
	--bam sorted_A01_62.fastq.bam \
	--bam sorted_A01_63.fastq.bam \
	-v output.vcf --genotype-qualities -p 1

filter variants
vcffilter -f "QUAL > 20" output.vcf > filtered_variants.vcf

decompose complex haplotypes
vcfallelicprimitives -k -g filtered_variants.vcf > filtered_decomposed_haplotype_variants.vcf

snpEff ann R64-1-1.105 filtered_decomposed_haplotype_variants.vcf > final.vcf

head -n 100 final.vcf > first100.vcf