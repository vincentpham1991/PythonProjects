#Name: Vincent Pham
from model import *

###########################
##        task2          ##
###########################
print"task 2:"
ticker,data = readFile("./data/stocks/training.csv","array")
DJIA = data[:,44]
tableListed = mkR2Table(data,DJIA)
print "table of R2 values for how well each stock variable predicts the Dow Jones Index: "
print tableListed

djiStocks = data[:,:30]
nondjiStocks = data[:,30:44]
allDJI = linear_regression(djiStocks,DJIA)
nonDJI = linear_regression(nondjiStocks,DJIA)
useAll = computeR2(allDJI, djiStocks, DJIA)
useNone = computeR2(nonDJI, nondjiStocks, DJIA)
print "\nprints out R2 for model that uses "
print "all of Dow Jones stocks: "
print useAll
print "none of the Dow Jones stocks: "
print useNone

###########################
##        task3          ##
###########################
print "\ntask 3:"
allStocks = data[:,:44]
bestModel, bestData, bestR2 = computeBestBivariate(allStocks,DJIA)
print "pair of variables that best predicts Dow Jones:"
print bestData
print "which corresponds to: "
for x in bestData:
    print ticker[x]
print "with an R^2 of: "
print bestR2

###########################
##        task4          ##
###########################
print "\ntask4:"
kModel, kData,kR2 = discoverKModel(allStocks,DJIA,5)
bestModel1, bestData1, bestR21 = discoverBestModel(allStocks,DJIA,.1)
bestModel2, bestData2, bestR22 = discoverBestModel(allStocks,DJIA,.01)
print "model used for computing the \"best\" K-variable model is choosing the K variables with the highest R^2 values in the table from Task 2."
print "using a threshold of .1, the best columns are: "
print bestData1
print "which corresponds to: "
for x in bestData1:
    print ticker[x]
print "with an R^2 of: "
print bestR21

print "\nusing a threshold of .01, the best columns are: "
print bestData2
print "which corresponds to: "
for x in bestData2:
    print ticker[x]
print "with an R^2 of: "
print bestR22
