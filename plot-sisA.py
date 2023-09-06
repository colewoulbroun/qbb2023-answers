#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# Get dataset to recreate Fig 3B from Lott et al 2011 PLoS Biology https://pubmed.gov/21346796
# wget https://github.com/bxlab/cmdb-quantbio/raw/main/assignments/lab/bulk_RNA-seq/extra_data/all_annotated.csv

transcripts = np.loadtxt("all_annotated.csv", delimiter=",", usecols=0, dtype="<U30", skiprows=1)
#print("transcripts: ", transcripts[0:5])

samples = np.loadtxt( "all_annotated.csv", delimiter=",", max_rows=1, dtype="<U30" )[2:]
#print("samples: ", samples[0:5])

data = np.loadtxt("all_annotated.csv", delimiter=",", dtype=np.float32, skiprows=1, usecols=range(2, len(samples) + 2))
#print("data: ", data[0:5, 0:5])

# Find row with transcript of interest
for i in range(len(transcripts)):
    if transcripts[i] == 'FBtr0073461':
        row = i

# Find columns with samples of interest
cols_female = []
cols_male = []
for i in range(len(samples)):
    if "female" in samples[i]:
        cols_female.append(i)
    else:
        cols_male.append(i)

# Subset data of interest
male_expression = data[row, cols_male]
female_expression = data[row, cols_female]

# Prepare data
x = samples
x = ["10", "11", "12", "13", "14A", "14B", "14C", "14D"]
y1 = male_expression
y2 = female_expression

# Plot data
fig, ax = plt.subplots()
ax.set_title("Developmental FBtr0073461 Expression in Females and Males")
ax.set_xlabel("Developmental Stage")
ax.set_ylabel("FBtr0073461 Expression")
ax.plot(x, y1, label = "Male")
ax.plot(x, y2, label = "Female")
ax.legend()
plt.xticks(rotation = 45, ha = "right")
plt.tight_layout()
fig.savefig("FBtr0073461_female_and_male.png")
plt.show()
#plt.close(fig)