def patient_mean(index,patient_data_file_path):
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

	average = sum(patient_data[index]) / len(patient_data[index])
	return average

patient_0 = 0
inflamation_data_file = "inflammation-01.csv"

print(patient_mean(patient_0, inflamation_data_file))