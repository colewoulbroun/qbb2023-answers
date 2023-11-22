#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Function to parse bedgraph files
def parse_bedgraph(file_path):
    columns = ["Chromosome", "Start", "End", "Percent_Methylation", "Coverage"]
    df = pd.read_csv(file_path, sep='\t', header=None, names=columns)
    return df


# Function to calculate comparisons and write to README.md
def compare_methylation_calls(bismark_file, nanopore_file, readme_file):
    # Calculate comparisons
    bismark_sites = set(zip(bismark_df["Chromosome"], bismark_df["Start"], bismark_df["End"]))
    nanopore_sites = set(zip(nanopore_df["Chromosome"], nanopore_df["Start"], nanopore_df["End"]))

    unique_bismark_sites = bismark_sites - nanopore_sites
    unique_nanopore_sites = nanopore_sites - bismark_sites
    shared_sites = bismark_sites.intersection(nanopore_sites)

    total_sites = len(bismark_sites.union(nanopore_sites))

    # Calculate percentages
    percent_unique_bismark = len(unique_bismark_sites) / total_sites * 100
    percent_unique_nanopore = len(unique_nanopore_sites) / total_sites * 100
    percent_shared = len(shared_sites) / total_sites * 100

    # Write results to README.md
    with open(readme_file, 'a') as readme:
        readme.write(f"\n# Methylation Calls Comparison\n")
        readme.write(f"- Sites present only in Bismark file: {len(unique_bismark_sites)} ({percent_unique_bismark:.2f}%)\n")
        readme.write(f"- Sites present only in Nanopore file: {len(unique_nanopore_sites)} ({percent_unique_nanopore:.2f}%)\n")
        readme.write(f"- Shared sites: {len(shared_sites)} ({percent_shared:.2f}%)\n")


# Function to plot distribution of coverages as a bar plot with specific x-axis limits
def plot_coverage_bar(bismark_df, nanopore_df, output_file):
    plt.figure(figsize=(12, 6))

    # Set specific x-axis limits
    x_axis_limits = (0, 100)

    # Plot Bismark coverage distribution
    plt.hist(bismark_df["Coverage"], range=x_axis_limits, alpha=0.5, label='Bismark', color='blue')

    # Plot Nanopore coverage distribution
    plt.hist(nanopore_df["Coverage"], range=x_axis_limits, alpha=0.5, label='Nanopore', color='orange')

    # Add labels and title
    plt.xlabel('Coverage')
    plt.ylabel('Frequency')
    plt.title('Coverage Distribution of CpG Sites')
    plt.legend()

    # Save or display the plot
    plt.savefig(output_file)
    plt.show()


# Function to plot the relationship between methylation scores
def plot_methylation_relationship(bismark_df, nanopore_df, output_file):
    plt.figure(figsize=(12, 8))

    # Select CpG sites occurring in both bedgraph files
    common_sites = pd.merge(bismark_df, nanopore_df, on=["Chromosome", "Start", "End"], suffixes=('_bismark', '_nanopore'))

    # Extract methylation scores
    methylation_bismark = common_sites["Percent_Methylation_bismark"]
    methylation_nanopore = common_sites["Percent_Methylation_nanopore"]

    # Create a 2D histogram
    hist, x_edges, y_edges = np.histogram2d(methylation_bismark, methylation_nanopore, bins=100)

    # Apply log10 transformation
    hist_log = np.log10(hist + 1)

    # Plot the transformed histogram using imshow
    plt.imshow(hist_log, extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], cmap='viridis', aspect='auto', origin='lower')

    # Add colorbar
    cbar = plt.colorbar()
    cbar.set_label('log10(Frequency + 1)')

    # Calculate Pearson R coefficient for non-transformed data
    r_coefficient = np.corrcoef(methylation_bismark, methylation_nanopore)[0, 1]

    # Add title with Pearson R coefficient
    plt.title(f'Methylation Relationship (Pearson R: {r_coefficient:.3f})')

    # Add labels
    plt.xlabel('Bismark Methylation Score (%)')
    plt.ylabel('Nanopore Methylation Score (%)')

    # Save or display the plot
    plt.savefig(output_file)
    plt.show()


#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Function to parse bedgraph files
def parse_bedgraph(file_path):
    columns = ["Chromosome", "Start", "End", "Percent_Methylation", "Coverage"]
    df = pd.read_csv(file_path, sep='\t', header=None, names=columns)
    return df


# Function to merge normal and tumor bedgraph data
def merge_bedgraphs(normal_df, tumor_df):
    merged_data = pd.merge(normal_df, tumor_df, on=["Chromosome", "Start", "End"], suffixes=('_normal', '_tumor'))
    return merged_data


# Function to calculate methylation changes (tumor - normal)
def calculate_methylation_changes(df):
    df['Methylation Change'] = df['Percent_Methylation_tumor'] - df['Percent_Methylation_normal']
    df = df[df['Methylation Change'].notna()]  # Exclude values with no change
    return df


# Function to plot violin plot of methylation changes
def plot_methylation_changes(methylation_change_common, output_file):
    plt.figure(figsize=(12, 8))

    # Plot violin plot
    sns.violinplot(x='Method', y='Methylation Change', data=methylation_change_common, inner='quartile')

    # Calculate Pearson R coefficient for methylation changes
    r_coefficient = np.corrcoef(
        methylation_change_common[methylation_change_common['Method'] == 'Nanopore']['Methylation Change'],
        methylation_change_common[methylation_change_common['Method'] == 'Bismark']['Methylation Change']
    )[0, 1]

    # Add Pearson R coefficient to the plot
    plt.text(0.5, 0.95, f'Pearson R: {r_coefficient:.3f}', transform=plt.gca().transAxes, ha='center', va='center', fontweight='bold', fontsize=12)

    # Add title and labels
    plt.title('Methylation Changes (Tumor - Normal) for Common Sites')
    plt.xlabel('Method')
    plt.ylabel('Methylation Change (%)')

    # Save or display the plot
    plt.savefig(output_file)
    plt.show()


# Parse bedgraphs
bismark_df = parse_bedgraph("bisulfite.cpg.chr2.bedgraph")
nanopore_df = parse_bedgraph("ONT.cpg.chr2.bedgraph")
normal_bismark_df = parse_bedgraph("normal.bisulfite.chr2.bedgraph")
tumor_bismark_df = parse_bedgraph("tumor.bisulfite.chr2.bedgraph")
normal_nanopore_df = parse_bedgraph("normal.ONT.chr2.bedgraph")
tumor_nanopore_df = parse_bedgraph("tumor.ONT.chr2.bedgraph")

# Compare methylation
compare_methylation_calls("bisulfite.cpg.chr2.bedgraph", "ONT.cpg.chr2.bedgraph", "week7_README.md")

# Plot coverage
plot_coverage_bar(bismark_df, nanopore_df, "coverage_distribution_plot.png")

# Plot relationship between methylation scores
plot_methylation_relationship(bismark_df, nanopore_df, "methylation_relationship_plot.png")

# Merge normal and tumor data
merged_data_bismark = merge_bedgraphs(normal_bismark_df, tumor_bismark_df)
merged_data_nanopore = merge_bedgraphs(normal_nanopore_df, tumor_nanopore_df)

# Find common sites
common_sites = set(merged_data_bismark.index).intersection(merged_data_nanopore.index)

# Calculate methylation changes
methylation_change_bismark = calculate_methylation_changes(merged_data_bismark.loc[list(common_sites)])
methylation_change_nanopore = calculate_methylation_changes(merged_data_nanopore.loc[list(common_sites)])

# Create dataframes for seaborn violin plot
changes_bismark_df = pd.DataFrame({
    'Method': ['Bismark'] * len(methylation_change_bismark),
    'Methylation Change': methylation_change_bismark['Methylation Change']
})

changes_nanopore_df = pd.DataFrame({
    'Method': ['Nanopore'] * len(methylation_change_nanopore),
    'Methylation Change': methylation_change_nanopore['Methylation Change']
})

# Concatenate the dataframes for both approaches
changes_df = pd.concat([changes_bismark_df, changes_nanopore_df], ignore_index=True)

# Plot methylation changes
plot_methylation_changes(changes_df, "methylation_changes_violin_plot.png")