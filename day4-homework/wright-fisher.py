# get a starting frequency and a population size
# input parameters for function

# while
# 	get the new allele frequency for next generation
# 	by drawing from the binomial distribution
# 	(convert number of successes into a frequency)

# 	store our allele frequency in the AF list

# return a list of allele frequency at each time point
# number of generations to fixation
# is the length of your list

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

allele_calculation = wright_fisher(allele_initial, pop_initial)

print("Allele frequencies for each generation before allele fixation:")
print(allele_calculation[0])

print("Generation number before allele fixation:")
print(allele_calculation[1])

fig, ax = plt.subplots()
x = range(allele_calculation[1])
y = allele_calculation[0]
plt.plot(x, y)
ax.set_title("Changes to Allele Frequency Over Generations")
ax.set_xlabel("Generation")
ax.set_ylabel("Allele Frequency")
plt.tight_layout()
plt.show()