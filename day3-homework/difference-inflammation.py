def patient_difference(index1, index2, patient_data_file_path):
	f = open(patient_data_file_path, "r")

	lines = f.readlines()

	patient_data = []

	for i in lines:
		i = i.rstrip()
		patient_strings = i.split(',')
		patient_integers = []
		for j in patient_strings:
			patient_integers.append(int(j))
		patient_data.append(patient_integers)

	patient_one_vs_two = []

	for y in range(40):
		patient_one = patient_data[index1][y]
		patient_two = patient_data[index2][y]
		one_vs_two = patient_one - patient_two
		patient_one_vs_two.append(one_vs_two)

	return(patient_one_vs_two)

patient_1 = 0
patient_2 = 1
inflamation_data_file = "inflammation-01.csv"

print(patient_difference(patient_1, patient_2, inflamation_data_file))