#!/usr/bin/env python

import sys

import numpy
import matplotlib.pyplot as plt
import scanpy as sc

# Read the 10x dataset filtered down to just the highly-variable genes
adata = sc.read_h5ad("variable_data.h5")
adata.uns['log1p']['base'] = None # This is needed due to a bug in scanpy

# Compute neighbor graph from adata
sc.pp.neighbors(adata, n_neighbors = 10, n_pcs = 40)

# Run leiden clustering on data
sc.tl.leiden(adata)

sc.tl.umap(adata, maxiter = 900)
sc.tl.tsne(adata)

fig, axes = plt.subplots(ncols = 2, figsize = (10,5))
sc.pl.umap(adata, ax = axes[0], color = 'leiden', title = 'UMAP', show = False)
sc.pl.tsne(adata, ax = axes[1], color = 'leiden', title = 'tSNE', show = False)
plt.tight_layout()
plt.savefig('Plots of UMAP and tSNE Dimensional Reduction')
plt.show()


wilcoxon_adata = sc.tl.rank_genes_groups(adata, method = 'wilcoxon', groupby = 'leiden', use_raw = True, copy = True)
logreg_adata = sc.tl.rank_genes_groups(adata, method = 'logreg', groupby = 'leiden', use_raw = True, copy = True)

fig2, axes2 = plt.subplots(nrows = 2, figsize = (10, 5))
sc.pl.rank_genes_groups(wilcoxon_adata, n_genes = 25, ax = axes2[0], title = 'Wilcoxon Top 25 Genes', sharey = False, show = False, use_raw = True, save = 'clustermarkers_wilcoxon.png')
sc.pl.rank_genes_groups(logreg_adata, n_genes = 25, ax = axes2[1], title = 'Logreg Top 25 Genes', sharey = False, show = False, use_raw = True, save = 'clustermarkers_logreg.png')
axes2[0].set_title(label = 'Wilcoxon Top 25 Genes')
axes2[1].set_title(label = 'Logreg Top 25 Genes')


sc.tl.umap(adata, maxiter = 900)
sc.tl.tsne(adata)

leiden = adata.obs['leiden']
umap = adata.obsm['X_umap']
tsne = adata.obsm['X_tsne']
adata = sc.read_h5ad('filtered_data.h5')
adata.obs['leiden'] = leiden
adata.obsm['X_umap'] = umap
adata.obsm['X_tsne'] = tsne

adata.write('filtered_clustered_data.h5')