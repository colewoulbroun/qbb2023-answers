#!/usr/bin/env python


import numpy

f = open("inflammation-01.csv", "r")

lines = f.readlines()

patient_data = []

for i in lines:
	i = i.rstrip()
	patient_strings = i.split(',')
	patient_integers = []
	for j in patient_strings:
		patient_integers.append(int(j))
	patient_data.append(patient_integers)

print("Fifth patient flare-ups on first, tenth, and last day.")
print(patient_data[4][0])
print(patient_data[4][9])
print(patient_data[4][-1])


patient_averages = []

for k in patient_data[0:-1]:
	patient_averages.append(numpy.mean(k))

print("Average daily flare-ups for first ten patients.")

for b in patient_data[0:10]:
	print(numpy.mean(b))


print("Highest and lowest average number of daily flare-ups for all patients.")

print(numpy.min(patient_averages))
print(numpy.max(patient_averages))


patient_one_vs_five = []

for y in range(40):
	patient_one = patient_data[0][y]
	patient_five = patient_data[4][y]
	one_vs_five = patient_one - patient_five
	patient_one_vs_five.append(one_vs_five)

print("Difference in daily flare-up number between patients 1 and 5.")

print(patient_one_vs_five)