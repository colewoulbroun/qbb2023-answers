#!/usr/bin/env python

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import multitest
from pydeseq2 import preprocessing
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import matplotlib.pyplot as plt
import seaborn as sns

# Read in data
counts_df = pd.read_csv('gtex_whole_blood_counts_formatted.txt', index_col = 0)

# Read in metadata
metadata = pd.read_csv('gtex_metadata.txt', index_col = 0)

# Process data and perform DDX11L11 regression
counts_df_normed = preprocessing.deseq2_norm(counts_df)[0]

counts_df_normed = np.log2(counts_df_normed + 1)

full_design_df = pd.concat([counts_df_normed, metadata], axis = 1)

model = smf.ols(formula = 'Q("DDX11L1") ~ SEX', data = full_design_df)
results = model.fit()

slope = results.params[1]
pval = results.pvalues[1]

# Create an empty DataFrame to store results
homemade_results_df = pd.DataFrame(index = counts_df_normed.columns, columns = ['slope', 'pval'])

# Perform regression for each gene and store results
for gene in counts_df_normed.columns:
    formula = f'Q("{gene}") ~ SEX'
    model = smf.ols(formula = formula, data = full_design_df)
    results = model.fit()
    
    homemade_results_df.loc[gene, 'slope'] = results.params[1]
    homemade_results_df.loc[gene, 'pval'] = results.pvalues[1]

# Write differentially expressed genes to text file
homemade_results_df.to_csv('homemade_correlated_genes.txt', sep = '\t')

# Read data from 'homemade_correlated_genes.txt'
homemade_correlated_results = pd.read_csv("homemade_correlated_genes.txt", index_col = 0, delimiter = '\t')

# Perform FDR correction
homemade_correlated_results['pval'] = homemade_correlated_results['pval'].fillna(1.0)
corrected_p_values = multitest.fdrcorrection(homemade_correlated_results['pval'], alpha = 0.05, method = 'indep', is_sorted = False)
homemade_correlated_results['qval'] = corrected_p_values[1]

# Write FDR corrected genes to text file
significant_corrected_pvalues = homemade_correlated_results[homemade_correlated_results['qval'] < 0.1]
significant_corrected_pvalues.to_csv('homemade_FDR_corrected_genes.txt', sep = '\t')


# Perform pydeseq2 regression
py_deseq2 = DeseqDataSet(counts = counts_df, metadata = metadata, design_factors = 'SEX', n_cpus = 4)

py_deseq2.deseq2()
py_deseq2_stats = DeseqStats(py_deseq2)
py_deseq2_stats.summary()
py_deseq2_results = py_deseq2_stats.results_df
py_deseq2_results.to_csv('pydeseq2_analysis_results.txt', sep = '\t')

significant_genes_homemade = pd.read_csv('homemade_FDR_corrected_genes.txt', sep = '\t', index_col = 0)
py_deseq2_genes = pd.read_csv('pydeseq2_analysis_results.txt', sep = '\t', index_col = 0)

# Calculate jaccard index
significant_genes_py_deseq2 = py_deseq2_genes.loc[py_deseq2_genes['padj'] < 0.1, :]

significant_genes_overlap = significant_genes_homemade[significant_genes_homemade.index.isin(significant_genes_py_deseq2.index)]

intersection_count = len(significant_genes_overlap)
union_count = len(significant_genes_homemade) + len(significant_genes_py_deseq2) - intersection_count
jaccard_index = (intersection_count / union_count) * 100

print(f'Jaccard index: {jaccard_index}%')


# Read in pydeseq2 differential expression analysis results
py_deseq2_results = pd.read_csv('pydeseq2_analysis_results.txt', sep='\t', index_col=0)

# Set significance threshold
fdr_threshold = 0.1
fold_change_threshold = 1.0

# Log transform p-values
py_deseq2_results['log_padj'] = -np.log10(py_deseq2_results['padj'])

# Create a subset of the data indicating significance
py_deseq2_results['significant'] = (py_deseq2_results['padj'] < fdr_threshold) & (abs(py_deseq2_results['log2FoldChange']) > fold_change_threshold)

# Create a volcano plot for all genes
plt.figure(figsize=(10, 6))
sns.scatterplot(x = py_deseq2_results['log2FoldChange'], y = py_deseq2_results['log_padj'], color = 'gray', alpha = 0.7, label = 'Non-significant Genes')

# Highlight significant genes in red with circle markers
highlighted_genes = py_deseq2_results[py_deseq2_results['significant']]
sns.scatterplot(x = highlighted_genes['log2FoldChange'], y = highlighted_genes['log_padj'], color = 'red', marker = 'o', s = 50, label = 'Significant genes (FDR < 10% & |log2FC| > 1)')

# Label and save the plot
plt.title('Sex-Based Differential Gene Expression in Whole Blood')
plt.xlabel('log2(Fold Change)')
plt.ylabel('-log10(Adjusted p-value)')
plt.legend(loc = 'lower left', fontsize = 6)
plt.savefig('volcano_plot.png')