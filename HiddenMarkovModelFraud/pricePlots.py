from pylab import *
import matplotlib.pyplot as plt
from scipy.cluster.vq import vq, kmeans, whiten
from numpy import *
def readFile(file):
	'''
	Read data from the specified file. Cleans the data
	and convert to floats
	
	Parameters
	-----------
	file: str
		name of the file to be read
			
	Returns
	---------
	dataset: array
		The array of prices 
	
	Note:
	------
	1st price listed is last purchased item (most recent).
	'''
	dataset = []
	
	file = open(file,"r")
	data = file.readlines()
	file.close
	
	data = data[1:]
	for rows in data:
		for ch in ['\xa0', '\n', ' ', '$',',', '"']:
			rows = rows.replace(ch,"")
		rows = float(rows)
		dataset.append(rows)
		
	return dataset


def genGraph(file):
	'''
	Generates the two non-optimal plots
	
	Parameters
	-----------
	file: str
		name of the file to be read
			
	Returns
	---------
	out: plots
	'''
	dataset,_,_,_ = clusterData(file,toPlot = True)
	plotData(dataset)
	eyeballCluster(dataset)
	
	return
	
	

def plotData(dataset):
	'''
	Plots the original dataset
	
	Parameters
	-----------
	dataset: array
		array to be plotted
			
	Returns
	---------
	out: plot
	'''
	tempX = [1]*len(dataset)
	plot(tempX,dataset,'bo')
	ylabel("Prices ($)")
	savefig("./graphs/plotData")
	clf()
	return

def eyeballCluster(dataset):
	'''
	Obtain cluster from looking plotData graph (Intuitive guess)
	
	Parameters
	-----------
	dataset: array
		array to be plotted
			
	Returns
	---------
	out: plot
	'''
	datacpy = dataset[:]
	datacpy.sort()
	low = []
	med = []
	high = []
	for x in datacpy:
		if (x < 250):
			low.append(x)
		elif (x < 700):
			med.append(x)
		else:
			high.append(x)
			
	xlow = [1]*len(low)
	xmed = [1]*len(med)
	xhigh = [1]*len(high)		
	
	plot(xlow,low,'ok', label = "low")
	plot(xmed,med,'oc', label = "medium")
	plot(xhigh,high,'oy', label = "high")
	legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=3,mode="expand",borderaxespad=0.)
	ylabel("Prices ($)")
	
	ticks = np.arange(0, max(datacpy)+100, 100)
	yticks(ticks)
		
	savefig("./graphs/eyeballCluster")
	clf()
	
	#bar plot of amounts
	y = [len(low),len(med),len(high)]
	N = len(y)
	ind = range(N)
	bar(ind,y)
	priceLabels = ['low', 'medium','high']
	title("eyeball cluster amount")
	ylabel("# of occurences")
	xlabel("categories")
	xticks(arange(len(priceLabels)),priceLabels, ha = 'center')
	
	savefig("./graphs/eyeballAmount")
	clf()
	
	return

def clusterData(file, toPlot = False):
	'''
	Provides data necesaarry for future cluster and produce optimal cluster data plots
	
	Parameters
	-----------
	file: str
		name of the file to be read
	toPlot: bool, optional
		When set to True, produces a cluster plot
		
	Returns
	---------
	dataset: array
		An array of price values
	catData: array
		An array of dataset converted to its respective categories
	med[0]: float
		The lowest value in the medium category
	high[0]: float
		The lowest value in the high category
	'''
	dataset = readFile(file)
	
	datacpy = dataset[:]
	datacpy.sort()
	numCat = 3

	optimal = False
	
	whitened = whiten(datacpy)
	
	while(optimal == False):
		count1 = 0
		count2 = 0
		count0 = 0
		
		centroids,_ = kmeans(whitened,numCat,50)
		idx,_ = vq(whitened,centroids)

		for x in idx:
			if(x==2):
				count2+=1
			elif(x==1):
				count1+=1
			else:
				count0+=1
		
		if(count2 > count1 and count1 > count0):
			optimal = True
	
	low = datacpy[0:count2]
	med = datacpy[count2:(count2+count1)]
	high = datacpy[(count2+count1):]
	
	if (toPlot == True):	
		xlow = [1]*len(low)
		xmed = [1]*len(med)
		xhigh = [1]*len(high)		
		
		plot(xlow,low,'ok', label = "low")
		plot(xmed,med,'oc', label = "medium")
		plot(xhigh,high,'oy', label = "high")
		
		ylabel("Prices ($)")
		
		ticks = np.arange(0, max(datacpy)+100, 100)
		yticks(ticks)
		
		legend(bbox_to_anchor=(0.,1.02,1.,.102),loc=3,ncol=3,mode="expand",borderaxespad=0.)

		savefig("./graphs/optimalCluster")
		clf()
		
		#bar plot of amounts
		y = [len(low),len(med),len(high)]
		N = len(y)
		ind = range(N)
		bar(ind,y)
		priceLabels = ['low', 'medium','high']
		title("optimal clustering amount")
		ylabel("# of occurences")
		xlabel("categories")
		xticks(arange(len(priceLabels)),priceLabels, ha = 'center')
		
		savefig("./graphs/optimalAmount")
		clf()
	
	catData = categorizeAll(dataset,med[0], high[0])
	
	return (dataset,catData, med[0], high[0])

def categorizeAll(dataset, medCutoff, highCutoff):
	'''
	Relabels the prices in its respective category (low, medium, or high)
	
	Parameters
	----------
	dataset: array
		The array of the price values
	medCutoff: float
		Marginal value between low and medium category
	highCutoff: float
		Marginal value between medium and high category
		
	Returns
	--------
	dataCat: array
		An array of the categorical data
	'''
	dataCat = []
	for x in dataset:
		if(x < medCutoff):
			dataCat.append("l")
		elif(x < highCutoff):
			dataCat.append("m")
		else:
			dataCat.append("h")
	
	return dataCat
	
def categorizeOne(data, medCutoff, highCutoff):
	'''
	Relabels the prices in its respective category (low, medium, or high)
	
	Parameters
	----------
	data: float
		A price values
	medCutoff: float
		Marginal value between low and medium category
	highCutoff: float
		Marginal value between medium and high category
		
	Returns
	--------
	val: str
		String of the categorical data
	'''
	if (data < medCutoff):
		return "l"
	elif (data < highCutoff):
		return "m"
	else:
		return "h"
	
	