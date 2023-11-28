Step 1.1

Plink command used for generating PCA:

plink --vcf genotypes.vcf --pca 10 --out genotype_pca



Step 2.1

Plink command used for calculating allele frequencies:

plink --vcf genotypes.vcf --freq --out allele_frequencies



Step 3.1

Plink command for GWAS with GS451:

plink --vcf genotypes.vcf --linear --pheno GS451_IC50.txt --covar genotype_pca.eigenvec --allow-no-sex --out GS451_GWAS


Plink command for GWAS with CB1908:

plink --vcf genotypes.vcf --linear --pheno CB1908_IC50.txt --covar genotype_pca.eigenvec --allow-no-sex --out CB1908_GWAS



Step 3.4

For my top GWAS hit with the GS451 genotype, the variant was within an intron of DIP2B (disco-interacting protein 2 homolog B).  DIP2B binds DNA methyltransferase 1 associated protein 1, and this interaction suggests a potential role in DNA methylation.  If this is true, and the variant at hand is affecting DNA methylation, then DNA methylation may be innolved in lymphocyte viability in the presence of cancer drugs.  This may be consistent with the reduced IC50 in the presence of the variant, which could be deleterious, as shown by the effect size.


For my top GWAS hit with the CB1908 genotype, the variant was within an intron of ZNF826, a zinc-finger protein.  The specific functions of ZNF826 are not well understood, but zinc-finger proteins are known transcription factors.  This gene could be involved in regulating a stress response to the CB1908 drug in lymphocytes.  The effect size of the variant on the IC50 was positve, presenting the possibility that ZNF826 could be preventing proper lymphocyte resisitance to cancer drugs.  Importantly, these hypotheses based on effect sizes are very speculative and require experimentation to provide stronger evidence.