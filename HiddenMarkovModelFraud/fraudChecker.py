#Authors: Vincent Pham and Sili Wen

from easygui import *
from HMMArray import *
from HMMGraph import drawGraphs
from pricePlots import *

def displayStore(file, nData = 100, threshhold = .5, fastTrack = True):
	'''
	Acts as an "online store" and ask user to make purchases and accepts
	or deny by using the HMM model. Also creates all figures necessary.
	
	Parameters
	----------
	file: str
		Use data file to train from
	nData: int or "All", optional,
		By default, nData = 100 for fast results.
		How much of the data to be trained.
		"All" for all data trained.
	threshhold: float, optional,
		deny percentage
	fasTrack: bool, optional
		By default, set to True and overrides nData
		with nData = 200 for a pre-obtained results
		
	Returns
	--------
	out: None
	
	Notes
	------
	identification password set to "1234"
	If red flag appears and identification false, you are a fraudster!
	else updates preferences (update total preferences after 10)
	
	value for fast track was obtained during an earlier run to save time.
	'''
	identification = "1234";
	
	dataset, dataCat, midCutoff, highCutoff = clusterData(file)
	datacpy = dataCat[:]
	datacpy.reverse()
	
	o1 = dataCat[-15:]
	t = len(o1)
	
	trainA = array([(.7,.3),(.8,.2)])
	trainPi = genPi(2)
	trainB = array([(0.1, 0.7, 0.2), (0.7, 0.1, 0.2)])
	
	alphabet = ['h','m','l']
	
	if (nData == "All"):
		oAll = datacpy[:]
	else:
		oAll = datacpy[-nData:]
		
	if (fastTrack == True):
		A = [[ 0.54671429, 0.45328571],[ 0.54706897, 0.45293103]]
		B = [[ 0.14285714, 0.83885714, 0.01828571],[ 0.14758621, 0.83034483, 0.02206897]]
		Pi = [ 0.5, 0.5]
	else:
		A, B, Pi = getEst(oAll, trainA, trainB, trainPi, alphabet)

	morePurchases = True
	
	a1 = getTotProb(o1, t, A, B, Pi, alphabet)
	
	count = 0
	
	while morePurchases != False:
		storeTitle = "This is a store"
		storeMsg = "Please enter amount of purchase."
		amount = float(enterbox(msg = storeMsg, title = storeTitle))
		amount = round(amount,2)
		amount = categorizeOne(amount, midCutoff, highCutoff)

		o2 = o1[1:]
		o2.append(amount)
		a2 = getTotProb(o2,t,A,B,Pi,alphabet)
		
		deltaA = abs(a1-a2)
		percentErr = deltaA/a1
		ask = False
		
		if (percentErr < threshhold):
			msgbox(msg = "Purchased made!")
			ask = True
			
		else:	
			password = passwordbox("please confirm your password")

			if (password == identification):
				msgbox(msg = "password confirmed! purchased made!")
				ask = True
			else:
				deniedImg = "./pix/denied.gif"
				deniedMsg = "access denied"
				deniedChoices = ["Flee!"]
				buttonbox(msg = deniedMsg, image = deniedImg, choices = deniedChoices)
				ask = False
				morePurchases = False
		
		probMsg = "the probility of observing [O1,...O15] given the model M = [A, B, Pi] is\n "+  str(a2)
		msgbox(msg = probMsg, title = "hidden message")
		
		if (ask == True):
			a1 = a2
			o1 = o2
			oAll = oAll[1:]
			oAll.append(amount)
			
			morePurchases = boolbox("do you want to make more purchases?")
			count += 1
			
		if (count >= 10):
			A, B, Pi = getEst(oAll, trainA, trainB, trainPi, alphabet)
			count = 0

	genGraph(file)
	drawGraphs(A,B)
	return

