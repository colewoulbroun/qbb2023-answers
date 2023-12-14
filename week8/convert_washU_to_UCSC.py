#!/usr/bin/env python

import sys


if len(sys.argv) != 4:
    print("Please provide the following inputs: baitmap file, WashU file, and output filepath")
    sys.exit(1)

baitmap_file, washu_file, output_file = sys.argv[1:]


# Function to convert WashU to UCSC format
def convert_washU_to_UCSC(baitmap_file, washu_file, output_file):
    # Read baitmap file and store information in a dictionary
    baitmap_data = {}

    with open(baitmap_file, 'r') as baitmap:
        for line in baitmap:
            # Split columns in each line of baitmap file
            chromosome_number, genomic_start, genomic_end, fragment_number, gene_name = line.strip().split('\t')
            baitmap_data[f'chr{chromosome_number},{genomic_start},{genomic_end}'] = gene_name


    # Read WashU file and convert to UCSC format
    with open(washu_file, 'r') as washu, open(output_file, 'w') as ucsc_output:
        # Add the track line at the beginning of the output file
        ucsc_output.write('track type = interact  name = "pCHIC"  description = "Chromatin interactions"  useScore = on  maxHeightPixels = 200:100:50  visibility = full\n')

        # Calculate interaction strength
        washu_content = list(washu)
        interaction_strengths = [float(line.strip().split('\t')[2]) for line in washu_content]

        # Make lists for different interactions
        bait_bait_interactions = []
        bait_target_interactions = []

        # Iterate through each line in the WashU file
        for line in washu_content:
            # Split columns in each line of WashU file, extract fragment and interaction information
            fields = line.strip().split('\t')
            fragment1_location, fragment2_location, interaction_strength = fields
            
            # Create variables to write information into each field of ucsc file
            chromosome_1 = fragment1_location.split(',')[0]
            start_2 = min(int(fragment1_location.split(',')[1]), int(fragment2_location.split(',')[1]))
            stop_3 = max(int(fragment1_location.split(',')[2]), int(fragment2_location.split(',')[2]))
            position_4 = '.'
            interaction_score_5 = int((float(interaction_strength) / max(interaction_strengths)) * 1000)
            raw_interaction_6 = interaction_strength
            position_7 = '.'
            position_8 = '0'

            if fragment1_location in baitmap_data and fragment2_location in baitmap_data:
            	bait_fragment, bait_gene = fragment1_location, baitmap_data[fragment1_location]
            	target_fragment, target_gene = fragment2_location, baitmap_data[fragment2_location]
            elif fragment1_location in baitmap_data:
            	bait_fragment, bait_gene = fragment1_location, baitmap_data[fragment1_location]
            	target_fragment, target_gene = fragment2_location, '.'
            elif fragment2_location in baitmap_data:
            	bait_fragment, bait_gene = fragment2_location, baitmap_data[fragment2_location]
            	target_fragment, target_gene = fragment1_location, '.'
            else:
            	print('Neither fragment is a bait.')
            	continue

            bait_chromosome_9 = bait_fragment.split(',')[0]
            bait_start_10 = bait_fragment.split(',')[1]
            bait_stop_11 = bait_fragment.split(',')[2]
            bait_gene_12 = bait_gene
            bait_strand_13 = '+'

            target_chromosome_14 = target_fragment.split(',')[0]
            target_start_15 = target_fragment.split(',')[1]
            target_stop_16 = target_fragment.split(',')[2]
            target_gene_17 = target_gene

            if fragment1_location in baitmap_data and fragment2_location in baitmap_data:
            	target_strand_18 = '+'
            else:
            	target_strand_18 = '-'

            # Identify interaction type and store in the appropriate list
            if fragment1_location in baitmap_data and fragment2_location in baitmap_data:
                bait_bait_interactions.append((line, interaction_strength))
            else:
                bait_target_interactions.append((line, interaction_strength))

            # Write fields into ucsc file
            ucsc_output.write(f'{chromosome_1}\t{start_2}\t{stop_3}\t{position_4}\t'
            	f'{interaction_score_5}\t{raw_interaction_6}\t{position_7}\t{position_8}\t '
            	f'{bait_chromosome_9}\t{bait_start_10}\t{bait_stop_11}\t '
            	f'{bait_gene_12}\t{bait_strand_13}\t{target_chromosome_14}\t '
            	f'{target_start_15}\t{target_stop_16}\t{target_gene_17}\t '
            	f'{target_strand_18}\n')

        # Sort interactions based on interaction strength
        bait_bait_interactions.sort(key = lambda x: float(x[1]), reverse = True)
        bait_target_interactions.sort(key = lambda x: float(x[1]), reverse = True)

        # Print the top 6 interactions of each type
        print("Top 6 Promoter-Promoter Interactions:")
        for interaction in bait_bait_interactions[:6]:
            print(interaction)

        print("\n\nTop 6 Promoter-Enhancer Interactions:")
        for interaction in bait_target_interactions[:6]:
            print(interaction)


convert_washU_to_UCSC(baitmap_file, washu_file, output_file)