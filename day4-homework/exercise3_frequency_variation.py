import numpy as np
import matplotlib.pyplot as plt

allele_initial = 0.46
pop_initial = 500

def wright_fisher(allele_freq, pop_size):

		allele_changes_list = []

		while 0 < allele_freq < 1:
			successes = np.random.binomial(2 * pop_size, allele_freq)
			allele_freq = successes / (2 * pop_size)
			allele_changes_list.append(allele_freq)

		return (allele_changes_list, len(allele_changes_list))

def mean(data):
	average = sum(data) / len(data)
	return average

average_fixation_time = []
allele_frequency = []

for j in range(10):
	allele_initial = allele_initial + 0.04
	allele_frequency.append(allele_initial)
	allele_freq_list = []
	allele_generation_list = []
	for i in range(200):
		i = wright_fisher(allele_initial, pop_initial)
		allele_freq_list.append(i[0])
		allele_generation_list.append(i[1])
	average_fixation_time.append(mean(allele_generation_list))

fig, ax = plt.subplots()
x = allele_frequency
y = average_fixation_time
ax.plot(x, y)
ax.set_title("Changes to Time to Allele Fixation with Allele Frequency")
ax.set_xlabel("Allele Frequency")
ax.set_ylabel("Time to Allele Fixation")
plt.tight_layout()
plt.show()