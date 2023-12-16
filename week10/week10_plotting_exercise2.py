#!/usr/bin/env python

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import scipy.stats as sps
import seaborn as sns


taylor_albums = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-10-17/taylor_albums.csv')

# Used print functions for each of the five columns in this dataframe for my initial data exploration


# Assessing correlation of user and metacritic scores for Taylor Swift albums

album_score_test = sps.ttest_ind(a = taylor_albums['metacritic_score'], b = taylor_albums['user_score'], equal_var = True, alternative = 'greater')
# The correlation between user and metacritic score for Taylor Swift's albums is not significant

fig, ax = plt.subplots()
ax.scatter(taylor_albums['metacritic_score'], taylor_albums['user_score'], label = 'Paternal', color = 'blue', marker = 'o')
ax.set_title("Taylor Swift Album Metacritic vs. User Score")
ax.set_xlabel("User Score")
ax.set_ylabel("Metacritic Score")
plt.tight_layout()
plt.savefig('taylor_album_score.png')


# Assessing frequency of album releases during career

album_release = taylor_albums['album_release']

album_release_year = []

for date in album_release:
	year = date.split('-')[0]
	year = int(year)
	album_release_year.append(year)

print(album_release_year)

plt.hist(album_release_year, color='blue', edgecolor='black')
plt.xlabel('Album Release Year')
plt.ylabel('Frequency')
plt.title('Frequency of Taylor Swift Album Releases')
plt.tight_layout()
plt.savefig('album_release_histogram.png')
# There seems to be a higher album release frequency in the early and more recent years of Taylor's career, with a dip in the middle


# Comparing metacritic ratings of original and re-released (Taylor's version) albums

re_releases = taylor_albums.iloc[11:13]
rerelease_scores = re_releases['metacritic_score']
rerelease_scores = list(rerelease_scores)

originals = pd.concat([taylor_albums.iloc[0:11], taylor_albums.iloc[13]], ignore_index = True)
original_scores = originals['metacritic_score']
original_score_list = []
for score in original_scores:
	if str(score) == 'nan':
		continue
	else:
		original_score_list.append(score)

categories = ['Re-released', 'Original']
scores = [rerelease_scores, original_score_list]

score_test = sps.ttest_ind(a = rerelease_scores, b = original_score_list, equal_var = True, alternative = 'greater')
# The correlation between metacritic score for original and re-released albums is not significant when using a threshold of p < 0.01

plt.bar(categories, [np.mean(score) for score in scores], yerr = [np.std(score) for score in scores], capsize = 5)
plt.title('Metacritic Scores of Original and Re-released Taylor Swift Albums')
plt.xlabel('Album Type')
plt.ylabel('Metacritic Score')
plt.savefig('original_vs_re-released_albums.png')