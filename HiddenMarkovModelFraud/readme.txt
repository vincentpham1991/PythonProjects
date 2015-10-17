Author: Vincent Pham and Sili Wen
Hidden Markov Model Application in Credit Card Fraud Detection

README: this file

fraudChecker.py: main file that connects all the others. Obtains the HMM values and ask users to input price to test the data. If price exeeds the threshhold, interface will ask for the password (1234). If password accepted, preferences will be updated and will ask user if they want to input more prices. If password is wrong, then user denied purchase and preferences is not updated. After 10 inputs, the whole model will be updated. Thus, software stops when you request no more purchases or when you enter the wrong password. For quick test, just type displayStore("dataHMM.csv"). More parameters can be added (read doc strings). Lower nData will be faster. Updates and saves graphs at end of function.

HMMArray.py: model for our HMM

HMMGraph.py: graphs the emission and transition probability

pricePlots.py:plots the credit card transactions and label them as low, medium, or high. Cluster analysis performed.

easygui.py: library not in standard version of python. Used to generate guis such as messageboxes. 


graphs (folder): where our graphs/plots are saved

pix (folder): pictures used for easyGui

dataHMM.csv: model price data obtained from Vincent's credit card debit transaction

categoryData.txt: output from HMMArray that gives the categories values of the prices in order

sherlock.txt: file used to initially test out HMM model (provided by Gustav)

Libraries needed:
NetworkX

Our sources of inspirations are:
1) Credit Card Fraud Detection Using Hidden Markov Model by Vaibhave Gade and Sonal Chaudhari, http://www.ijetae.com/files/Volume2Issue7/IJETAE_0712_89.pdf

2) Credit Card Fraud Detection Using Hidden Markov Model by Shailesh S. DHOK, http://www.ijsce.org/attachments/File/v2i1/A0385012111.pdf