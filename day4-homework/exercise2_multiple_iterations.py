import numpy as np
import matplotlib.pyplot as plt

allele_initial = 0.5
pop_initial = 100

def wright_fisher(allele_freq, pop_size):

	allele_changes_list = []

	while 0 < allele_freq < 1:
		successes = np.random.binomial(2 * pop_size, allele_freq)
		allele_freq = successes / (2 * pop_size)
		allele_changes_list.append(allele_freq)

	return (allele_changes_list, len(allele_changes_list))

fixation_time = []

for i in range(1000):
	i = wright_fisher(allele_initial, pop_initial)
	fixation_time.append(i[1])

fig, ax = plt.subplots()
ax.hist(fixation_time, bins = 10)
ax.set_title("Generations to Allele Fixation in Wright-Fisher Model")
ax.set_xlabel("Generations to Allele Fixation")
ax.set_ylabel("Frequency")
plt.tight_layout()
plt.show()