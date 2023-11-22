Question 1:
Are the majority of the CpG dinucleotides methylated or unmethylated?

The majority of CpG dinucleotides are methylated.  The ONT.cpg.chr2.bedgraph and bisulfite.cpg.chr2.bedgraph files show that the majority of dinucleotides have a percent methylation over 50%, with many having a percent methylation at or near 100%.


# Methylation Calls Comparison
- Sites present only in Bismark file: 132466 (2.96%)
- Sites present only in Nanopore file: 53346 (1.19%)
- Shared sites: 4296642 (95.85%)


Question 2:
How does using nanopore for methylation calling differ from bisulfite sequencing in terms of coverage? Which method appears better and why?

Based on the coverage plot, bisulfite sequencing for methylation calling seems to provide higher, more uniform coverage than nanopore.  Given this higher coverage and increased coverage uniformity, I would consider bisulfite sequencing as the better method.


Question 3: What can you infer about the two different approaches and their ability to detect methylation changes?

Given the similarity of the methylation changes between normal and tumor samples detected by bisulfite and nanopore approaches, I have more confidence that both techniques can accurately detect changes in methylation between samples.  If the techniques were inaccurate, it is unlikely that they would be inaccurate in the same way.


Question 4: What is the effect of tumorigenesis on global methylation patterns?

Based on the nanopore and bisulfite sequencing data, it appears that tumorigenesis has little effect on the global methylation pattern.  Most CpG islands do not have a change in methylation between normal and tumor samples.  However, the violin plots indicate a smaller number of CpG islands that undergo either large increases or decreases in methylation.  This suggests that tumorigenesis could have more sequence-specific, rather than global, effects on CpG methylation.


Question 5: What changes can you observe between the normal and tumor methylation landscape? What do you think the possible effects are of the changes you observed?

I noticed differences between normal and tumor methylation around the first exon and 5' region of DNMT3A.  There is increased methylation of this site in the tumor relative to normal cells.  These differences in DNA methylation at the 5' region of a gene, which contains the transcriptional start site and promoter, are commonly found in DNA methylation research.  Importantly, this increased methylation of the tumor DNMT3A 5' region suggests that DNMT3A expression may be reduced in tumors, which could reduce the rate of de novo DNA methylation.


Question 6: What does it mean for a gene to be “imprinted”? 

An imprinted gene has differential expression based on the parent from which it is inherited.  If a gene is imprinted, expression of the paternal gene is different than expression of the maternal gene across development and adulthood.  DNA methylation is involved in generating the differential expression observed in imprinting.


Question 7: What is happening when you select the option to phase the reads? What is required in order to phase the reads?

When I select the option to phase the reads at the ZDBF2 gene, IGV is attempting to determine which alleles from the existing pool of reads lie on the same chromosome.  In this case, these alleles are methylated and unmethylated CpG islands.  Pre-exisiting haplotype information is required for read phasing.  A haplotype is a set of alleles on adjacent chromosomes that are inherited together, so haplotype information can be used to identify and sort reads that originate from a common chromosome.


Question 8: Can any set of reads be phased? Explain your answer.

No, not every set of reads can be phased.  Read phasing relies on knowledge of haplotypes in the genomic region of interest.  If there is limited understanding of distinguishing features in this region, read phasing will be more difficult.  Read phasing is also much easier in non-repetitive, unique regions of the genome that have identifiable haplotypes.  Haplotyping is more difficult in regions with strucutral variants and/or repetition.