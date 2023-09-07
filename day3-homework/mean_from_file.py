def mean(data):
	average = sum(data) / len(data)
	return average

f = open("my_integers.txt", "r")

lines = f.readlines()

integer_data = []

for i in lines:
	i = i.rstrip()
	integer_data.append(int(i))

my_mean = mean(integer_data)

print(my_mean)