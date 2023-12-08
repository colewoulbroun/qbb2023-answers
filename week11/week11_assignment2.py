#!/usr/bin/env python

import sys

import numpy
import matplotlib.pyplot as plt
import scanpy as sc

adata = sc.read_h5ad("filtered_clustered_data.h5")
adata.uns['log1p']['base'] = None # This is needed due to a bug in scanpy 

fig, axes = plt.subplots(ncols = 3, figsize = (10, 5))
sc.pl.umap(adata, ax = axes[0], color = 'CD79A', title = 'CD79A Expression', show = False)
sc.pl.umap(adata, ax = axes[1], color = 'CD3D', title = 'CD3D Expression', show = False)
sc.pl.umap(adata, ax = axes[2], color = 'CST3', title = 'CST3 Expression', show = False)
plt.tight_layout()
plt.savefig('CD79A_CD3D_CST3_UMAP.png')

cell_types = {'CD79A': 'B-cell', 'CD3D': 'T-cell', 'CST3': 'Myeloid'}

new_clusters = [0, 1, 'B-cell', 3, 'T-cell', 5, 'Myeloid', 7]

adata.rename_categories('leiden', new_clusters)

fig, ax = plt.subplots()
sc.pl.umap(adata, ax = ax, color = 'leiden', title = 'UMAP', show = False)
plt.tight_layout()
plt.savefig('Cell_Type-Labeled_Clusters.png')
plt.show()