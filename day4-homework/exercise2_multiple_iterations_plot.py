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

allele_freq_list = []
allele_generation_list = []

for i in range(30):
	i = wright_fisher(allele_initial, pop_initial)
	allele_freq_list.append(i[0])
	allele_generation_list.append(i[1])

fig, ax = plt.subplots()
for i in range(30):
	x = range(allele_generation_list[i])
	y = allele_freq_list[i]
	ax.plot(x, y)
ax.set_title("Changes to Allele Frequency Over Generations")
ax.set_xlabel("Generation")
ax.set_ylabel("Allele Frequency")
plt.tight_layout()
plt.show()