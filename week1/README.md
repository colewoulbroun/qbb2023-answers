Step 2.2: Now that you’ve visualized these relationships, you’re curious whether they’re statistically significant. Perform ordinary least squares using the smf.ols() function to test for an association between maternal age and maternally inherited de novo mutations. In your README.md for this assignment, answer the following questions:

	1. What is the “size” of this relationship? In your own words, what does this mean? Does this match what you observed in your plots in step 2.1?

	The size of the relationship between maternal age and maternal de novo mutations is 0.3776.  This calculation states that the number of de novo mutations a mother will pass on to her child increases by approximately 0.3776 with each year of age.  This positive correlation between maternal age and de novo mutations matches the results observed in my Step 2.1 scatter plot, as this also indicates a gradual, linear increase in maternal de novo mutations with the mother's age.

	2. Is this relationship significant? How do you know?

	This relationship is significant, as the p-value for the correlation is 0.000, below the typical significance threshold of 0.05.  This value indicates that there is a 0.000 (0%) chance of the coefficient, or size, for the whole population, rather than just the coefficient of the sample depicted in this data, being zero.  This provides strong evidence for a correlation between maternal age and de novo mutations.


Step 2.3: As before, perform ordinary least squares using the smf.ols() function, but this time to test for an association between paternal age and paternally inherited de novo mutations. In your README.md for this assignment, answer the following questions:

	1. What is the “size” of this relationship? In your own words, what does this mean? Does this match what you observed in your plots in step 6?

	The size of the relationship between paternal age and paternal de novo mutations is 1.3878.  This value states that the number of mutations a father will pass on to his offspring increases by 1.3878 with each year of age.  This positive correlation, which is steeper than the correlation between maternal age and de novo mutations, matches the results observed in my scatter plot from Step 2.1.  There is a steep, linear increase in paternal de novo mutations with age.

	2. Is this relationship significant? How do you know?

	The relationship is significant, as the p-value for the correlation is 0.000.  This, again, is below the typical significance threshold of 0.05 for p-values.  As previously stated, this value indicates that there is a 0.000 (0%) chance that the coefficient, or size, of the whole population is 0.  The calculation must work on probability, as only a sample of the population is surveyed in this data.


Step 2.4: Using your results from step 2.3, predict the number of paternal DNMs for a proband with a father who was 50.5 years old at the proband’s time of birth. Record your answer and your work (i.e. how you got to that answer) in your README.md.

	For this question, I used the .predict function in python to get an estimate of the de novo mutations passed down from a father who is 50.5 years old.  While I knew that a .predict function had to be used, I also had to call on the correct data and enter a command for age prediction.  Since my "paternal_results" variable contained the linear regression for my paternal data, I wrote paternal_results.predict().  Within the parenthesis, I then specified that I wanted a prediction in the "paternal_dnm" category from the "Father_age" category for an age of 50.5 years.  My completed line was as follows: print(paternal_results.predict({'Father_age': 50.5})).  This line produced a de novo mutation value of 81.314386.


Step 2.6: Now that you’ve visualized this relationship, you want to test whether there is a significant difference between the number of maternally vs. paternally inherited DNMs per proband. What would be an appropriate statistical test to test this relationship? Choose a statistical test, and find a Python package that lets you perform this test. If you’re not sure where to look, the stats module from scipy (more here) provides tools to perform several different useful statistical tests. After performing your test, answer the following answers in your README.md for this assignment:

	1. What statistical test did you choose? Why?

	For this question, I chose a two-sample t-test for independent samples.  This test provides a probability output for whether the mean of the population of one independent sample is either significantly different (for two-tailed) or significantly greater than/less than (for one-tailed) the mean of the population of another independent sample.  Our two samples are paternal and maternal de novo mutations, and by looking at the histogram, it is clear that there are more paternal mutations.  Furthermore, the data on paternal mutations is not affected by the data on maternal mutations and vice versa, they are independent.  Therefore, assessing the significance of this difference with a one-tailed t-test was a strong approach to the question.

	2. Was your test result statistically significant? Interpret your result as it relates to the number of paternally and maternally inherited DNMs.

	My test was statistically significant, as I got a p-value of about 1.395e-273, which is well below the typical threshold of 0.05.  Since I performed a one-tailed t-test, the results of this test state that the mean number of paternal de novo mutations is significantly greater than the mean number of maternal de novo mutations.