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



# Step 3.2

# Function to read GWAS files
def read_gwas_results(filename):
    gwas_results = pd.read_csv(filename, delim_whitespace = True)
    return gwas_results


# Function to plot Manhattan
def plot_manhattan(gwas_results, drug_name, threshold):

    if drug_name == 'CB1908':
    	round_number = 0
    else:
    	round_number = 1

    gwas_results_plot = gwas_results[gwas_results['TEST'] == 'ADD']

    significant_snps = gwas_results_plot[gwas_results_plot['P'] < threshold]
    ax[round_number].scatter(significant_snps.index, -1 * np.log(significant_snps['P']), color = 'red', label = 'Significant, p < 1e-5', zorder = 5)

    non_significant_snps = gwas_results_plot[gwas_results_plot['P'] > threshold]
    ax[round_number].scatter(non_significant_snps.index, -1 * np.log(non_significant_snps['P']), color = 'blue', label = 'Non-significant, p > 1e-5')

    ax[round_number].legend(loc = 'upper right', fontsize = 8, bbox_to_anchor = (1.2, 1), borderaxespad = 0.)
    ax[round_number].set_title(f'Manhattan Plot - {drug_name}')
    ax[round_number].set_xlabel('SNP Index')
    ax[round_number].set_ylabel('-log10(p-value)')
    ax[round_number].set_ylim(bottom = -0.5)


# Set up plot
fig, ax = plt.subplots(nrows = 2, ncols = 1, figsize = (12, 12))

# Reading the GWAS files
gwas_results_gs451 = read_gwas_results('GS451_GWAS.assoc.linear')
gwas_results_cb1908 = read_gwas_results('CB1908_GWAS.assoc.linear')

# Plotting
plot_manhattan(gwas_results_cb1908, 'CB1908', 1e-5)
plot_manhattan(gwas_results_gs451, 'GS451', 1e-5)

plt.tight_layout()
plt.savefig('manhattan_plot.png')



# Step 3.3

# Identify lowest p-value
def lowest_p_value(gwas_data):
    lowest_p_value = gwas_data['P'].idxmin()
    snp_id = gwas_data['SNP'][lowest_p_value]

    return lowest_p_value, snp_id


# Retrieve phenotypes
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


# Retrieve genotypes
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

    return homozygous_1, heterozygous, homozygous_2


lowest_p_value, snp_id = lowest_p_value(gwas_results_cb1908)

phenotype_list = retrieve_phenotypes('CB1908_IC50.txt')

homozygous_no_variant, heterozygous, homozygous_variant = extract_phenotypes_from_vcf('genotypes.vcf', snp_id, phenotype_list)


# Plot data
genotype_categories = [homozygous_no_variant, heterozygous, homozygous_variant]
genotype_labels = ['Homozygous - Wild Type', 'Heterozygous', 'Homozygous - Variant']

plt.boxplot(genotype_categories, labels = genotype_labels)
plt.title(f'Effect Size of SNP ({snp_id}) on CB1908 IC50')
plt.xlabel('Genotype')
plt.ylabel('Phenotype Score')
plt.xticks(rotation = 30)
plt.tight_layout()
plt.savefig('effect_size_boxplot.png')