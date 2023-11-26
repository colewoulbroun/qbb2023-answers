#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


# empty lists for each set of data

read_depths = []
genotyping_qualities = []
allele_frequencies = []
predicted_effects = []


# open file and parse data

for line in open('final.vcf'):
	if line.startswith('#'):
		continue
	fields = line.rstrip('\n').split('\t')


# extract read depth

	format_fields = fields[8].split(':')
	for sample_field in fields[9:]:
		dp_index = format_fields.index('DP')
		sample_info = sample_field.split(':')
		initial_depth = sample_info[dp_index]
		if initial_depth != '.':
			final_read_depth = int(initial_depth)
			read_depths.append(final_read_depth)
		else:
			continue


# extract genotype qualities across samples

	for sample_field in fields[9:]:
		gq_index = format_fields.index('GQ')
		sample_info = sample_field.split(':')
		genotype_quality = sample_info[gq_index]
		if genotype_quality != '.':
			genotype_quality = float(genotype_quality)
			genotyping_qualities.append(genotype_quality)
		else:
			continue


# extract allele frequency, incorporating alleles from complex variants as separate alleles (Dylan said this was an option for extraction and analysis)

	af_info = fields[7].split(';')
	for info in af_info:
		if info.startswith('AF='):
			frequencies_initial = info.split('=')[1]
			allele_freq = frequencies_initial.split(',')
			for freq in allele_freq[:]:
				final_allele_frequency = float(freq)
				allele_frequencies.append(final_allele_frequency)
		else:
			continue


# extract predicted effects

	ann_info = fields[7].split(';')
	for info in ann_info:
		if info.startswith('ANN='):
			annotations_initial = info.split('=')[1]
			annotations = annotations_initial.split('|')
			for ann in annotations[1:]:
				if ann == '' or ',' in ann:
					continue
				else:
					predicted_effects.append(ann)


# plot the data

# create a 2x2 subplot grid
fig, axs = plt.subplots(2, 2, figsize=(15, 12))


# plot histogram of read depths. to make sure I followed the instructions by making a read depth histogram for each variant, even the outliers with very high coverage, I coverted the raw frequency values to log10 values so all the data could be visualized well
axs[0, 0].hist(read_depths, bins = range(min(read_depths), max(read_depths) + 1), align = 'left', color = 'red')
axs[0, 0].set_title('Read Depths Across Samples')
axs[0, 0].set_xlabel('Read Depths')
axs[0, 0].set_ylabel('Frequency (log10 scale)')
axs[0, 0].set_xlim(left = -2)
axs[0, 0].set_yscale('log')


# plot histogram of genotype quality. given the 10-fold higher frequencies of certain genotype quality values, I plotted frequencies on the log10 scale so all the data could be visualized well
bin_edges = np.arange(min(genotyping_qualities), max(genotyping_qualities) + 1.5, 1)
axs[0, 1].hist(genotyping_qualities, bins = bin_edges, align = 'left', color = 'orange')
axs[0, 1].set_title('Genotype Quality Across Samples')
axs[0, 1].set_xlabel('Genotype Quality')
axs[0, 1].set_ylabel('Frequency (log10 scale)')
axs[0, 1].set_xlim(-2, 170)
axs[0, 1].set_yscale('log')


# plot histogram of allele frequencies
bin_width = 0.1
bin_edges = np.arange(min(allele_frequencies), max(allele_frequencies) + bin_width, bin_width)
axs[1, 0].hist(allele_frequencies, bins = bin_edges, align = 'left', color = 'green')
axs[1, 0].set_title('Allele Frequencies Across Samples')
axs[1, 0].set_xlabel('Allele Frequencies')
axs[1, 0].set_ylabel('Frequency')
axs[1, 0].set_xlim(left = -0.1)


# plot bar plot of predicted effects
effect_counts = {}

for effect in predicted_effects:
    if effect in effect_counts:
        effect_counts[effect] += 1
    else:
        effect_counts[effect] = 1

sorted_effects = sorted(effect_counts.items(), key=lambda x: x[1], reverse = True)

total_counts = sum(effect_counts.values())

top_number = 6
top_effects, top_counts = zip(*sorted_effects[:top_number])

proportions = [count / total_counts for count in top_counts]

axs[1, 1].bar(top_effects, proportions, color = 'blue')
axs[1, 1].set_title('Top 6 Predicted Effects')
axs[1, 1].set_xlabel('Effect Type')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].set_xticks(range(len(top_effects)))
axs[1, 1].set_xticklabels(top_effects, rotation = 45)


plt.tight_layout()
plt.savefig('vcf_multiplot.png')