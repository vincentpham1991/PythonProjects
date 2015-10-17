#Name: Vincent Pham
from model import *
###########################
##        task1          ##
###########################
ticker, data = readFile("./data/stocks/training.csv","array")
BA = data[:,2]
DJIA = data[:,44]
GOOG = data[:,-13]
IBM = data[:,12]

singleVariable(BA,"BA",DJIA,"DJIA","task1(BA vs DJIA)")
singleVariable(GOOG,"GOOG",DJIA,"DJIA", "task1(GOOG vs DJIA)")
singleVariable(IBM, "IBM",DJIA,"DJIA","task1(IBM vs DJIA)")

###########################
##        task4          ##
###########################
stocks = data[:,:44]
N = len(stocks[0])
R2 = [discoverKModel(stocks, DJIA, x)[2] for x in range(1,N)]
plot(range(1,N),R2,".")
xlabel("K")
ylabel("R^2")
savefig("./pix/task4")
clf()

###########################
##        task5          ##
###########################
tickerTesting, dataTesting = readFile("./data/stocks/testing.csv","array")
nondjiStocks = data[:,30:44]
SP = data[:,45]
testingDJIA = dataTesting[:,44]
testingSP = dataTesting[:,45]
testingNon = dataTesting[:,30:44]
modelTable = genModelTable(nondjiStocks, DJIA, testingNon, testingDJIA)
K = []
testing = []
training = []
for day in modelTable:
    K.append(day[0])
    testing.append(day[1])
    training.append(day[2])
plot(K,testing,".",label="testing")
plot(K,training,"*",label="training")
xlabel("K")
ylabel("R^2")
title("Dow Jones")
legend(loc="upper left")
savefig("./pix/task5(djia)")
clf()

modelTableSP = genModelTable(nondjiStocks,SP,testingNon,testingSP)
spK = []
spTesting = []
spTraining = []
for day in modelTableSP:
    spK.append(day[0])
    spTesting.append(day[1])
    spTraining.append(day[2])
plot(spK,spTesting,".",label="testing")
plot(spK,spTraining,"*",label="training")
xlabel("K")
ylabel("R^2")
title("S&P")
legend(loc="upper left")
savefig("./pix/task5(S&P)")
clf()
