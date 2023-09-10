import numpy as np
import matplotlib.pyplot as plt

allele_initial = 0.5
pop_initial = 50

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
population_size = []

for j in range(10):
	pop_initial = pop_initial + 50
	population_size.append(pop_initial)
	allele_freq_list = []
	allele_generation_list = []
	for i in range(50):
		i = wright_fisher(allele_initial, pop_initial)
		allele_freq_list.append(i[0])
		allele_generation_list.append(i[1])
	average_fixation_time.append(mean(allele_generation_list))

fig, ax = plt.subplots()
x = population_size
y = average_fixation_time
ax.plot(x, y)
ax.set_title("Changes to Generations to Allele Fixation with Population Size")
ax.set_xlabel("Population Size")
ax.set_ylabel("Average Generations to Allele Fixation")
plt.tight_layout()
plt.show()