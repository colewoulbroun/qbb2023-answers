test_list = [1, 9, 2, 3, 7, 5, 5, 4, 2, 8, 4, 9, 12]

def mean(data):
	average = sum(data) / len(data)
	return average

my_mean = mean(test_list)

print(my_mean)