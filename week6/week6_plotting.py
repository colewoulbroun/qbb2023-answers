#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Step 1.2

# Read the first two principal components from genotype_pca.eigenvec
with open('genotype_pca.eigenvec', 'r') as file:
    lines = file.readlines()


sample_ids = []
pc1_values = []
pc2_values = []


for line in lines:
    parts = line.split()
    sample_ids.append(parts[0])
    pc1_values.append(float(parts[2]))
    pc2_values.append(float(parts[3]))


# Create a scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(pc1_values, pc2_values, alpha=0.5)
plt.title('Genotype Principal Components')
plt.xlabel('PC1')
plt.ylabel('PC2')


# Save the plot
plt.savefig('genotype_pca_plot.png')



# Step 2.2

# Read allele frequencies from the .frq file
afs_file = 'allele_frequencies.frq'
with open(afs_file, 'r') as file:
    lines = file.readlines()


# Extract allele frequencies from the file
allele_frequencies = [float(line.split()[4]) for line in lines[1:]]


# Create a histogram of allele frequencies
plt.figure(figsize=(10, 6))
plt.hist(allele_frequencies, bins = 50, edgecolor = 'black', alpha = 0.7)
plt.title('Allele Frequency Spectrum')
plt.xlabel('Allele Frequency')
plt.ylabel('Frequency Count')


# Save the plot
plt.savefig('allele_frequency_spectrum.png')



# # Step 3.2

def read_gwas_results(filename):
    gwas_results = pd.read_table(filename, delim_whitespace = True)
    return gwas_results


def plot_manhattan(ax, gwas_results, drug_name, threshold):
    gwas_results['log_p_value'] = -np.log10(gwas_results['P'])
    chromosomes = sorted(set(gwas_results['CHR']))

    for chrom in chromosomes:
        subset = gwas_results[gwas_results['CHR'] == chrom]

        # Sort SNPs within each chromosome by base pair number
        subset = subset.sort_values(by = 'BP')

        non_significant_color = plt.cm.Blues((chrom / len(chromosomes)) + 0.1)
        significant_color = plt.cm.Reds((chrom / len(chromosomes)) + 0.1)

        # Adjust horizontal position within each chromosome segment
        x_positions = np.arange(len(subset))

        # Plot SNPs based on chromosome position and base pair number
        ax.scatter(subset['CHR'], subset['log_p_value'], label = f'Chr {chrom}', alpha = 0.5, color = non_significant_color, s = 10, edgecolors = 'none')

        significant_snps = subset[subset['P'] < threshold]
        ax.scatter(significant_snps['CHR'], significant_snps['log_p_value'], label = f'Chr {chrom} (Significant, p < 1e-5)', alpha = 0.7, color = significant_color, s = 10, edgecolors = 'none')

    ax.set_title(drug_name)
    ax.set_xlabel('Chromosome Number')
    ax.set_ylabel('-log10(p-value)')
    ax.legend(loc = 'upper right', fontsize = 5.5, bbox_to_anchor = (1.2, 1), borderaxespad = 0.)

# Reading the GWAS files
gwas_results_gs451 = read_gwas_results('GS451_GWAS.assoc.linear')
gwas_results_cb1908 = read_gwas_results('CB1908_GWAS.assoc.linear')

# Create a two-panel figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (12, 12))

# Make manhattan plot, highlighting SNPs with p-values < 1e-5 in a different color
plot_manhattan(ax1, gwas_results_gs451, 'GS451', 1e-5)
plot_manhattan(ax2, gwas_results_cb1908, 'CB1908', 1e-5)

# Save the figure
plt.tight_layout()
plt.savefig('manhattan_plot.png')



# Step 3.3

# identify lowest p-value
def lowest_p_value(gwas_data):
    lowest_p_value = gwas_data['P'].idxmin()
    snp_id = gwas_data['SNP'][lowest_p_value]

    return lowest_p_value, snp_id


# retrieve phenotypes
def retrieve_phenotypes(phenotype_data):
    with open(phenotype_data, 'r') as data:
    	data_for_phenotypes = data.readlines()

    phenotype_lists = []

    for line in data_for_phenotypes:
    	values = line.strip().split('\t')
    	phenotype_lists.append(values)

    phenotypes = []

    for phenotype in phenotype_lists:
    	if phenotype[2] == 'CB1908_IC50':
    		continue
    	else:
    		phenotypes.append(phenotype[2])

    return phenotypes


# retrieve genotypes
def extract_phenotypes_from_vcf(vcf_filename, snp_id, phenotype_values):
    homozygous_1 = []
    homozygous_2 = []
    heterozygous = []

    with open(vcf_filename, 'r') as vcf_file:
        for variant in vcf_file:
            if variant.startswith('#'):
                continue
            fields = variant.rstrip('\n').split('\t')
            if fields[2] == snp_id:
                genotypes = fields[9:]
                for index, genotype in enumerate(genotypes):
                    try:
                        phenotype_val = float(phenotype_values[index])
                        if genotypes[index] == '0/0' and not np.isnan(phenotype_val):
                            homozygous_1.append(phenotype_val)
                        elif genotypes[index] == '1/1' and not np.isnan(phenotype_val):
                            homozygous_2.append(phenotype_val)
                        elif genotypes[index] in ('0/1', '1/0') and not np.isnan(phenotype_val):
                            heterozygous.append(phenotype_val)
                    except ValueError:
                    	continue
                break

    return homozygous_1, homozygous_2, heterozygous


lowest_p_value, snp_id = lowest_p_value(gwas_results_cb1908)

phenotype_list = retrieve_phenotypes('CB1908_IC50.txt')

homozygous_no_variant, homozygous_variant, heterozygous = extract_phenotypes_from_vcf('genotypes.vcf', snp_id, phenotype_list)


# plot data
genotype_categories = [homozygous_no_variant, homozygous_variant, heterozygous]
genotype_labels = ['Homozygous - Wild Type', 'Homozygous - Variant', 'Heterozygous']

plt.boxplot(genotype_categories, labels = genotype_labels)
plt.title(f'Effect Size of SNP ({snp_id}) on CB1908 IC50')
plt.xlabel('Genotype')
plt.ylabel('Phenotype Score')
plt.xticks(rotation = 30)
plt.tight_layout()
plt.savefig('effect_size_boxplot.png')