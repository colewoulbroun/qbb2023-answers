#!/usr/bin/env python

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

import scipy.stats as sps
import statsmodels.formula.api as smf
import statsmodels.api as sm


# Step 1.1
df = pd.read_csv("/Users/cmdb/cmdb-quantbio/assignments/bootcamp/statistical_modeling/extra_data/aau1043_dnm.csv")

# Step 1.2
deNovoCount = {}

for _, row in df.iterrows():
    proband_id = row['Proband_id']
    phase_combined = row['Phase_combined']

    if proband_id not in deNovoCount:
    	deNovoCount[proband_id] = [0, 0]

    if phase_combined == "mother":
    	deNovoCount[proband_id][0] = deNovoCount[proband_id][0] + 1
    else:
    	deNovoCount[proband_id][1] = deNovoCount[proband_id][1] + 1

# Step 1.3
deNovoCountDF = pd.DataFrame.from_dict(deNovoCount, orient = 'index', columns = ['maternal_dnm', 'paternal_dnm'])

# Step 1.4
df1 = pd.read_csv("/Users/cmdb/cmdb-quantbio/assignments/bootcamp/statistical_modeling/extra_data/aau1043_parental_age.csv", index_col = 0)

# Step 1.5
combined_df = pd.concat([deNovoCountDF, df1], axis = 1)


# Step 2.1
fig, ax = plt.subplots()
ax.scatter(combined_df.iloc[:, 2], combined_df.iloc[:, 1], label = 'Paternal', color = 'blue', marker = 'o')
ax.set_title("Paternal De Novo Mutations vs. Paternal Age")
ax.set_xlabel("Paternal Age")
ax.set_ylabel("Paternal De Novo Mutations")
plt.tight_layout()
plt.show()

fig, ax = plt.subplots()
ax.scatter(combined_df.iloc[:, 3], combined_df.iloc[:, 0], label = 'Maternal', color = 'pink', marker = 'o')
ax.set_title("Maternal De Novo Mutations vs. Maternal Age")
ax.set_xlabel("Maternal Age")
ax.set_ylabel("Maternal De Novo Mutations")
plt.tight_layout()
plt.show()

# Step 2.2 and 2.3
maternal_ordinary_least_squares = smf.ols('maternal_dnm ~ Mother_age', combined_df)
maternal_results = maternal_ordinary_least_squares.fit()

paternal_ordinary_least_squares = smf.ols('paternal_dnm ~ Father_age', combined_df)
paternal_results = paternal_ordinary_least_squares.fit()

print(maternal_results.summary())
print(paternal_results.summary())

# Step 2.4
print(paternal_results.predict({'Father_age': 50.5}))

# Step 2.5
fig, ax = plt.subplots()
ax.hist(combined_df.iloc[:, 1], color = 'blue', edgecolor ='blue', alpha = 0.25)
ax.hist(combined_df.iloc[:, 0], color = 'pink', edgecolor = 'pink', alpha = 0.25)
ax.set_title("Maternal vs. Paternal De Novo Mutation Frequency")
ax.set_xlabel("De Novo Mutation Count")
ax.set_ylabel("Frequency")
plt.tight_layout()
plt.show()

# Step 2.6
stats_test = sps.ttest_ind(a = combined_df.iloc[:, 1], b = combined_df.iloc[:, 0], equal_var = True, alternative = 'greater')

print(stats_test)