#!/usr/bin/env python

import numpy as np
import pandas as pd
import seaborn as sns
from pydeseq2 import preprocessing
from matplotlib import pyplot as plt


# Step 1.0: Load the data

# read in data
counts_df = pd.read_csv("gtex_whole_blood_counts_formatted.txt", index_col=0)

# read in metadata
metadata = pd.read_csv("gtex_metadata.txt", index_col=0)

# normalize
counts_df_normed = preprocessing.deseq2_norm(counts_df)[0]

# log
counts_df_logged = np.log2(counts_df_normed + 1)

# merge with metadata
full_design_df = pd.concat([counts_df_logged, metadata], axis=1)


# Step 1.1: Gene expression for GTEX-113JC

data_gtex113jc = counts_df_logged.loc['GTEX-113JC'][counts_df_logged.loc['GTEX-113JC'] > 0]

plt.hist(data_gtex113jc, bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Logged Normalized Counts')
plt.ylabel('Frequency')
plt.title('Distribution of Gene Expression in GTEX-113JC')
plt.savefig('expression_distribution_GTEX-113JC.png')


# Step 1.2: MXD4 expression differences between sexes 

data_mxd4_males = full_design_df[full_design_df['SEX'] == 1]['MXD4']
data_mxd4_females = full_design_df[full_design_df['SEX'] == 2]['MXD4']

plt.figure(figsize = (10, 6))
plt.hist(data_mxd4_males, label = 'Male', bins = 30, color = 'blue', alpha = 0.7, edgecolor = 'black')
plt.hist(data_mxd4_females, label = 'Female', bins = 30, color = 'pink', alpha = 0.7, edgecolor = 'black')
plt.legend()
plt.title('MXD4 Expression in Males vs Females')
plt.xlabel('Logged Normalized Counts')
plt.ylabel('Frequency')
plt.savefig('mxd4_expression_malesvsfemales.png')


# Step 1.3: Distribution of subject ages

subject_ages = full_design_df['AGE']
counts = subject_ages.value_counts()
order = ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79"]
counts = counts.loc[order]

plt.figure(figsize=(10, 6))
plt.bar(counts.index, counts, color='blue', alpha=0.7, edgecolor='black')
plt.title('Age Distribution of Subjects')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.savefig('subject_age_distribution.png')


# Step 1.4: Sex-stratfied expression with age

lpxn_age_sex = full_design_df[['AGE', 'SEX', 'LPXN']]

expression_data = lpxn_age_sex.groupby(['AGE', 'SEX'])['LPXN'].median().reset_index()
male_female_categories = {1: 'Male', 2: 'Female'}
expression_data['SEX'] = expression_data['SEX'].map(male_female_categories)
plt.figure(figsize = (12, 8))
sns.barplot(x = 'AGE', y = 'LPXN', hue = 'SEX', data = expression_data, errorbar = None)
plt.legend(loc = 'upper right')
plt.title('Median Sex-Stratified Gene Expression Over Lifecourse')
plt.xlabel('Age')
plt.ylabel('Median Logged Normalized Counts')
plt.savefig('sex_stratified_gene_expression_with_age.png')