#!/usr/bin/env python

import sys
import scipy.stats
import numpy
import matplotlib.pyplot as plt
from scipy.stats import poisson

# Step 1: Calling Peaks

# def main():

#     if len(sys.argv) != 6:
#         print("Usage: python livecodingweek4.py <forward_fname> <reverse_fname> <controlf_fname> <controlr_fname> <out_fname>")
#         sys.exit(1)

#     forward_fname, reverse_fname, controlf_fname, controlr_fname, out_fname = sys.argv[1:]

#     # defining the fragment width here based on estimated size from live coding
#     fragment_width = 198

#     # specifying the genomic region to analyze
#     chrom = "chr2R"
#     chromstart = 10000000
#     chromend = 12000000
#     chromlen = chromend - chromstart

#     # combining forward and reverse data
#     combined_sample_bedgraph = combine_bedgraphs(forward_fname, reverse_fname, chrom, chromstart, chromend, 2 * fragment_width)

#     combined_control_bedgraph = combine_bedgraphs(controlf_fname, controlr_fname, chrom, chromstart, chromend, 2 * fragment_width)

#     # comparing to background and calculations
#     control_background = calculate_background(combined_control_bedgraph, chrom, chromstart, chromend, width=1000)
    
#     # scoring samples and generating p-values
#     sample_scores = score_sample(combined_sample_bedgraph, fragment_width)
    
#     sample_pvalues = calculate_pvalues(sample_scores, control_background)

#     # write wiggle and bed files
#     write_wiggle(sample_pvalues, chrom, chromstart, out_fname + ".wig")

#     write_bed(sample_pvalues, chrom, chromstart, chromend, fragment_width, out_fname + ".bed")

#     significant_peaks = []

#     # print the peaks with their chromosomal location
#     print("Significantly enriched peaks:")
#     position = chromstart
#     for index, p_value in enumerate(sample_pvalues):
#         if -numpy.log10(p_value) >= 10:  # Adjust the threshold as needed
#             start = position
#             end = position + fragment_width
#             significant_peaks.append((start, end, -numpy.log10(p_value)))
#             print(f"Chromosome: {chrom}, Start: {start}, End: {end}, -log10 P-value: {-numpy.log10(p_value)}")
#         position = position + 1

#     # print the number of significantly enriched peaks
#     significant_peaks_number = len(significant_peaks)
#     print(f"Number of significantly enriched peaks: {significant_peaks_number}")


# # define additional functions
# def load_bedgraph(fname, target, chromstart, chromend):
#     # Create array to hold tag counts
#     coverage = numpy.zeros(chromend - chromstart, int)

#     #Read the file in line by line
#     for line in open(fname):
#         # Break the line into individual fields
#         chrom, start, end, score = line.rstrip().split('\t')
#         # Check if the data fall in our target region
#         if chrom != target:
#             continue
#         start = int(start)
#         end = int(end)
#         if start < chromstart or end >= chromend:
#             continue
#         # Add tags to our array
#         coverage[start-chromstart:end-chromend] = int(score)
#     return coverage


# def combine_bedgraphs(forward_fname, reverse_fname, chrom, chromstart, chromend, shift):
#     # Load the forward and reverse bedgraph data
#     forward_bedgraph = load_bedgraph(forward_fname, chrom, chromstart, chromend)
#     reverse_bedgraph = load_bedgraph(reverse_fname, chrom, chromstart, chromend)

#     # Combine the forward and reverse data and shift by 'shift'
#     combined_bedgraph = [f + r for f, r in zip(forward_bedgraph, reverse_bedgraph)]
#     return combined_bedgraph


# def calculate_background(control_bedgraph, chrom, chromstart, chromend, width):
#     background = []

#     for i in range(chromend - chromstart):
#         start = max(0, i - width // 2)
#         end = min(chromend - chromstart, i + width // 2 + 1)

#         # Calculate the mean of control_bedgraph within the window
#         mean_value = sum(control_bedgraph[start:end]) / (end - start)

#         background.append(mean_value)

#     return background


# def score_sample(sample_bedgraph, fragment_width):
#     scores = []

#     for i in range(len(sample_bedgraph)):
#         start = max(0, i - fragment_width)
#         end = min(len(sample_bedgraph), i + fragment_width + 1)

#         # Calculate the score by summing the sample bedgraph values within the window
#         score = sum(sample_bedgraph[start:end])

#         scores.append(score)

#     return scores


# def calculate_pvalues(sample_scores, control_background):
#     pvalues = []

#     for score, background_mean in zip(sample_scores, control_background):
#         p = 1 - poisson.cdf(score, background_mean)

#         pvalues.append(p)

#     return pvalues


# def write_wiggle(pvalues, chrom, chromstart, fname):
#     output = open(fname, 'w')
#     print(f"fixedStep chrom={chrom} start={chromstart + 1} step=1 span=1", file=output)
#     for i in pvalues:
#         print(i, file=output)
#     output.close()


# def write_bed(pvalues, chrom, chromstart, chromend, width, fname):
#     chromlen = chromend - chromstart
#     enriched_peaks = []

#     for position, p_value in enumerate(pvalues):
#         if -numpy.log10(p_value) >= 10:  
#             start = position + chromstart
#             end = start + width
#             enriched_peaks.append((chrom, start, end, -numpy.log10(p_value)))

#     with open(fname, 'w') as output:
#         for peak in enriched_peaks:
#             print(f"{peak[0]}\t{peak[1]}\t{peak[2]}\t{peak[3]}", file=output)


# if __name__ == "__main__":
#     main()


# Step 2: Intersecting Peaks

if len(sys.argv) != 4:
    print("Usage: python week4_assignment.py <sample1.bed> <sample2.bed> <combined_peaks.bed>")
    sys.exit(1)

sample1_bed = sys.argv[1]
sample2_bed = sys.argv[2]
combined_peaks_bed = sys.argv[3]

def bedgraph_peak_count(bedgraph_fname):
    with open(bedgraph_fname, 'r') as f:
        peaks = f.readlines()
    return len(peaks)

print("Sample 1 Peaks:")
sample_1_peak_count = bedgraph_peak_count(sample1_bed)
print(sample_1_peak_count)

print("Sample 2 Peaks:")
sample_2_peak_count = bedgraph_peak_count(sample2_bed)
print(sample_2_peak_count)

print("Overlapping Peaks:")
combined_peaks_count = bedgraph_peak_count(combined_peaks_bed)
print(combined_peaks_count)