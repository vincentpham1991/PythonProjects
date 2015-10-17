# Name: Vincent Pham
import math

# reads in a dataset 
def read_data_from_dir(path, variables):
	dataset = []
	
	for line in variables:
		dataset.append(read_single_data(path, line))
		
	return dataset

#reads the file of each variables and returns the raw returns
def read_single_data(path, variable):
	adjClose = []
	allData = []
	rawReturn = []
	
	file = open(path + "/"+variable+".csv", "r")
	data = file.readlines()
	file.close
	
	data = data[1:]
	for days in data:
		allData.append(days.strip().split(","))
	
	for days in allData:
		adjClose.append(float(days[-1]))
	
	N = len(adjClose)
	for x in range(1,N):
		rawReturn.append(math.log(adjClose[x]) - math.log(adjClose[x-1]))
	
	return rawReturn
	
#gets number of days in a dataset
def get_number_of_days(dataset):
	numDays = len(dataset[0])
	return numDays

#computes correlation between 2 variables
def compute_correlation(datalist1, datalist2, interval_start, interval_length):
	sumproduct = 0.0
	square1 = 0.0
	square2 = 0.0

	datalist1 = datalist1[interval_start: interval_start+interval_length]
	datalist2 = datalist2[interval_start: interval_start+interval_length]
	
	mean1 = sum(datalist1)/(interval_length)
	mean2 = sum(datalist2)/(interval_length)
	
	for x in range(interval_length):
		sumproduct = sumproduct + (datalist1[x] - mean1)*(datalist2[x] - mean2)
		square1 = square1 + (datalist1[x] - mean1)**2
		square2 = square2 + (datalist2[x] - mean2)**2
		
	cov = sumproduct/(interval_length-1)
	var1 = square1/(interval_length - 1)
	var2 = square2/(interval_length - 1)
	std1 = math.sqrt(var1)
	std2 = math.sqrt(var2)
	correlation = cov/(std1*std2)
	
	return correlation

#computes the correlation matrix between several variables during a time period
def compute_correlation_matrix(dataset, variables, interval_start, interval_length):

	N = len(variables)
	numDays = get_number_of_days(dataset)

	#crash gracefully
	if interval_length < 2 or interval_start + interval_length > numDays:
		correlation_matrix = [[-1.0 for x in range(N)] for y in range (N)]
	else:
		correlation_matrix = [[compute_correlation(dataset[x],dataset[y],interval_start,interval_length) for x in range(N)] for y in range (N)]
			
	return correlation_matrix

