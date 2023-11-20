#!/usr/bin/env python


import sys
import numpy as np
from fasta import readFASTA
import pandas as pd


def alignment_algorithm(sequences, scoring_matrix, gap_penalty):

	input_sequences = readFASTA(open(sequences))

	sequence1_id, sequence1 = input_sequences[0]
	sequence2_id, sequence2 = input_sequences[1]

	scoring_matrix = pd.read_csv(scoring_matrix, header=0, index_col=0, delim_whitespace=True)

	gap_penalty = int(gap_penalty)

	F_matrix = np.zeros((len(sequence1) + 1, len(sequence2) + 1))

	traceback_matrix = np.zeros((len(sequence1) + 1, len(sequence2) + 1), dtype = int)

	for i in range(1, len(sequence1) + 1):
		F_matrix[i, 0] = i * gap_penalty
		traceback_matrix[i, 0] = 3

	for j in range(1, len(sequence2) + 1):
		F_matrix[0, j] = j * gap_penalty
		traceback_matrix[0, j] = 2

	for i in range(1, len(sequence1) + 1):
		for j in range(1, len(sequence2) + 1):
			aligned_score = scoring_matrix.at[sequence1[i-1], sequence2[j-1]]
			d = F_matrix[i-1, j-1] + aligned_score
			h = F_matrix[i, j-1] + gap_penalty
			v = F_matrix[i-1, j] + gap_penalty
			F_matrix[i, j] = max(d, h, v)

			moves = [(d, 1), (h, 2), (v, 3)]

			moves.sort(reverse=True, key=lambda x: x[0])

			max_score = moves[0][0]

			traceback_matrix[i, j] = moves[0][1]

		for move_score, move_direction in moves[1:]:
			if move_score == max_score:
				if move_direction == 1:
					traceback_matrix[i, j] = move_direction
				elif move_direction == 2 and traceback_matrix[i, j] != 1:
					traceback_matrix[i, j] = move_direction
				elif move_direction == 3 and traceback_matrix[i, j] != 1 and traceback_matrix[i, j] != 2:
					traceback_matrix[i, j] = move_direction

		alignment_score = F_matrix[-1, -1]

	return F_matrix, traceback_matrix, alignment_score


def find_optimal_alignment(F_matrix, traceback_matrix, sequences, gap_penalty):
    
    input_sequences = readFASTA(open(sequences))

    sequence1_id, sequence1 = input_sequences[0]
    sequence2_id, sequence2 = input_sequences[1]

    i, j = len(sequence1), len(sequence2)
    aligned_sequence1 = ""
    aligned_sequence2 = ""

    while i > 0 or j > 0:
        if traceback_matrix[i, j] == 1:
            aligned_sequence1 = sequence1[i - 1] + aligned_sequence1
            aligned_sequence2 = sequence2[j - 1] + aligned_sequence2
            i -= 1
            j -= 1
        elif traceback_matrix[i, j] == 2:
            aligned_sequence1 = "-" + aligned_sequence1
            aligned_sequence2 = sequence2[j - 1] + aligned_sequence2
            j -= 1
        else:
            aligned_sequence1 = sequence1[i - 1] + aligned_sequence1
            aligned_sequence2 = "-" + aligned_sequence2
            i -= 1

    return aligned_sequence1, aligned_sequence2


DNA_sequence_file = sys.argv[1]
DNA_scoring_matrix_file = sys.argv[2]
DNA_gap_penalty = int(sys.argv[3])
protein_sequence_file = sys.argv[4]
protein_scoring_matrix_file = sys.argv[5]
protein_gap_penalty = int(sys.argv[6])
output_dna_file = sys.argv[7]
output_protein_file = sys.argv[8]


aligned_sequences = {}

F_matrix_DNA, traceback_matrix_DNA, alignment_score_DNA = alignment_algorithm(DNA_sequence_file, DNA_scoring_matrix_file, DNA_gap_penalty)
F_matrix_protein, traceback_matrix_protein, alignment_score_protein = alignment_algorithm(protein_sequence_file, protein_scoring_matrix_file, protein_gap_penalty)

aligned_DNA_sequence1, aligned_DNA_sequence2 = find_optimal_alignment(F_matrix_DNA, traceback_matrix_DNA, DNA_sequence_file, DNA_gap_penalty)
aligned_sequences.update({"DNA Sequence 1": aligned_DNA_sequence1, "DNA Sequence 2": aligned_DNA_sequence2})

aligned_protein_sequence1, aligned_protein_sequence2 = find_optimal_alignment(F_matrix_protein, traceback_matrix_protein, protein_sequence_file, protein_gap_penalty)
aligned_sequences.update({"Protein Sequence 1": aligned_protein_sequence1, "Protein Sequence 2": aligned_protein_sequence2})


for key, sequence in aligned_sequences.items():
	gap_list = []
	for base in sequence:
		if base == "-":
			gap_list.append(base)
	print(f"{key} Gap Number: {len(gap_list)}")


print(f"DNA Alignment Score: {alignment_score_DNA}")
print(f"Protein Alignment Score: {alignment_score_protein}")


output_dna = open(output_dna_file, "w")
output_protein = open(output_protein_file, "w")

output_dna.write("DNA Sequence 1: " + "\n" + aligned_DNA_sequence1 + "\n")
output_dna.write("\n\n")
output_dna.write("DNA Sequence 2: " + "\n" + aligned_DNA_sequence2)

output_protein.write("Protein Sequence 1: " + "\n" + aligned_protein_sequence1 + "\n")
output_protein.write("\n\n")
output_protein.write("Protein Sequence 2: " + "\n" + aligned_protein_sequence2)

output_dna.close()
output_protein.close()