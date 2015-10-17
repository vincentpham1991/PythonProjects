import re, string, numpy, pylab
from numpy import *

def getAlphabet(obs):
	'''
	Retrieves the possible observation values. 

	Parameters
	----------
	obs: list of observations
		
	Returns
	--------
	out: the alphabet as a list
	'''
	alphabet = []
	for word in obs:
		for c in word:
			if c in alphabet:
				pass
			else:
				alphabet.append(c)
	return alphabet

def genPi(nStates): 
	'''
	Generates a uniform initial matrix. For our sake, this is actually not too important

	Parameters
	----------
	nStates: number of states in the model
		
	Returns
	--------
	out: a uniform 1XN array
	'''
	val = 1./nStates
	Pi = zeros(nStates)

	for s in range(nStates):
		Pi[s] = val
	return Pi
	
def normalizeArrayRow(array):
	dims = array.shape
	for row in range(dims[0]):
		rowSum = sum(array[row])
		for col in range(dims[1]):
			array[row][col] /= rowSum
	return array

def genA(nStates):
	'''
	Generates a uniform state transition matrix

	Parameters
	----------
	nStates: number of states in model 

	Returns
	--------
	A: a uniform transition matrix
	'''
	val = 1/nStates
	A = zeros((nStates, nStates))

	for from_s in range(nStates):
		for to_s in range(nStates):
			A[from_s][to_s] = val
	return A

def forward(obs, A, B, Pi, alphabet):
	'''
	The 'forward' component of the forward-bacwkard algorithm. The forward variable
	alpha(i, t) expresses the total probabilty of ending up in state i at time t, given the observations o1...ot-1 we have seen
	It is calculated by summing the probabilities for all incomig arcs at a node

	Parameters
	----------
	obs: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	alpha: a list of length len(O)+1
	'''
	N = len(obs)
	nStates = len(Pi) #number of states
	alpha = zeros((nStates, N + 1))
	
	#initialization
	for s in range(nStates):
		alpha[s][0] = Pi[s]
	#induction
	for t in range(1, N+1):
		o = obs[t-1] #o is the observation at time t
		oVal = alphabet.index(o) #oVal is the index of o in our alphabet. we need this to lookup a value in our B matrix
		for to_state in range(nStates):
			alpha[to_state][t] = 0
			for from_state in range(nStates):
				alpha[to_state][t] += alpha[from_state][t-1]*A[from_state][to_state]*B[from_state][oVal]
	return alpha


def backward(obs, A, B, Pi, alphabet):
	'''
	The 'backward' component of the forward-bacwkard algorithm. The backward variable
	beta(i, t) expresses the total probabilty of seeing the rest of the obseravtion sequence given we were in state i at time t.
	We need this moreso to use the forward-backward algorithm

	Parameters
	----------
	obs: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	beta: a list of length len(O)+1
'''
	N = len(obs)
	nStates = len(Pi)
	beta = zeros((nStates, N+1))

	#initialization
	for s in range(nStates):
		beta[s][N] = 1
	#induction
	for t in range(N-1, -1, -1):
		o = obs[t]
		oVal = alphabet.index(o)
		for from_state in range(nStates):
			beta[from_state][t] = 0
			for to_state in range(nStates):	
				beta[from_state][t] += beta[to_state][t+1]*A[from_state][to_state]*B[from_state][oVal]	
	return beta
	

def getTotProb(O, t, A, B, Pi, alphabet):
	'''
	The forward-bacwkard algorithm. gives the probability of witnessing an observation sequence, given a model.

	Parameters
	----------
	obs: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: P(O given our model A, Bi, Pi)
	'''
	alph = forward(O, A, B, Pi, alphabet)
	bet = backward(O, A, B, Pi, alphabet)
	rv = 0
	N = len(O)+1
	nStates = len(Pi)
	
	for state in range(nStates): 
		rv += alph[state][t]*bet[state][t]
	return rv

def prob_itoj_t(O, t, from_state, to_state, A, B, Pi, alphabet):
	'''
	Get the expected count of the number of transitions from state i to state j at time t

	Parameters
	----------
	obs: visible observations
	t: time
	from_state: state i
	to_state: state j
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	num/denom: the desired number above
	'''
	alph = forward(O, A, B, Pi, alphabet)
	bet = backward(O, A, B, Pi, alphabet)
	o = O[t]
	oVal = alphabet.index(o)

	denom = getTotProb(O, t, A, B, Pi, alphabet)
	num = alph[from_state][t]*A[from_state][to_state]*B[from_state][oVal]*bet[to_state][t+1]
	return (num/denom)
	
def getGamma(f_state, O, t, A, B, Pi, alphabet):
	'''
	Gets number of expected transitions out of state i at time t

	Parameters
	----------
	f_state: state i
	O: visible observations
	t: time
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: the expected no. of transitions out of state i
	'''
	rv = 0
	nStates = len(Pi)

	for to_state in range(nStates):
		val = prob_itoj_t(O, t, f_state, to_state, A, B, Pi, alphabet)
		rv += val
	return rv

	
def getExpecteditoj(fr_state, to_state, O, A, B, Pi, alphabet):
	'''
	Gets number of expected transitions out of state i to state j


	Parameters
	----------
	f_state: state i
	to_state: state j
	O: visible observations
	t: time
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: the expected no. of transitions out of state i to state j
	'''
	rv = 0
	N = len(O)

	for t in range(N):
		val = prob_itoj_t(O, t, fr_state, to_state, A, B, Pi, alphabet)
		rv += val
	return rv

def getExpectedFromi(fr_state, O, A, B, Pi, alphabet):
	'''
	Gets number of expected transitions out of state i to state j in the entire sequence

	Parameters
	----------
	f_state: state i
	O: visible observations
	t: time
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: the expected no. of transitions out of state i to state j in the entire sequence
	'''
	rv = 0
	N = len(O)
	for t in range(N):
		val = getGamma(fr_state, O, t, A, B, Pi, alphabet)
		rv += val
	return rv

def getExpectediObsK(fr_state, k, O, A, B, Pi, alphabet):
	'''
	Get the expected number of transitions out of state i given we produce the obseravtion k


	Parameters
	----------
	f_state: state i
	k: the observation
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: the expected no. of transitions out of state i given we emit k
	'''
	rv = 0
	N = len(O)
	nStates = len(Pi)

	for t in range(N):
		for to_state in range(nStates):
			if (O[t-1] == k):
				val = prob_itoj_t(O, t, fr_state, to_state, A, B, Pi, alphabet)
				rv += val
	return rv
	
def getAVal(fr_state, to_state, O, A, B, Pi, alphabet):
	'''
	Expectation step:
	Expected number of transitions from state i to state j, so our value for A[i][j]

	Parameters
	----------
	f_state: state i
	to_state: state j
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	num/denom: the value for expected A[i][j]
	'''
	num = getExpecteditoj(fr_state, to_state, O, A, B, Pi, alphabet)
	denom = getExpectedFromi(fr_state, O, A, B, Pi, alphabet)
	return num/denom

def getBVal(fr_state, k, O, A, B, Pi, alphabet):
	'''
	Expectation step:
	Expected number of transitions from state i emitting observation k, so our value for B[i][k]

	Parameters
	----------
	f_state: state i
	k: observation
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	num/denom: the value for expected B[i][k]
	'''
	num = getExpectediObsK(fr_state, k, O, A, B, Pi, alphabet)
	denom = getExpectedFromi(fr_state, O, A, B, Pi, alphabet)
	return num/denom
	
def getPi1(O, A, B, Pi, alphabet):
	'''
	Expectation step:
	Expected number of initial transitions out of state i, so our value for Pi[i]

	Parameters
	----------
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	num/denom: the value for expected Pi[i]
	'''
	nStates = len(Pi)
	rv = zeros(Pi.shape)

	for state in range(nStates):
		rv[state] = getGamma(state, O, 0, A, B, Pi, alphabet)
	return rv

def getA1(O, A, B, Pi, alphabet):
	'''
	Run getAVal on all combinations of state i and state j to find a reestimated A matrix

	Parameters
	----------
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: reestimated A matrix
	'''
	nStates = len(Pi)
	rv = zeros(A.shape)

	for fr_state in range(nStates):
		for to_state in range(nStates):
			rv[fr_state][to_state] = getAVal(fr_state, to_state, O, A, B, Pi, alphabet)
	return rv

def getB1(O, A, B, Pi, alphabet):
	'''
	Run getBVal on all combinations of state i and emission k to find a reestimated B matrix

	Parameters
	----------
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	rv: reestimated B matrix
	'''
	nStates = len(Pi)
	rv = zeros(B.shape)
	
	for fr_state in range(nStates):
		for letter in alphabet:
			oVal = alphabet.index(letter) - 1
			rv[fr_state][oVal] = getBVal(fr_state, letter, O, A, B, Pi, alphabet)
	return rv

def dist(a, b):
	return abs(a-b)

#test condition to see if the transition matricies are converging
def aConvTest(A, estA):
	dims = A.shape
	for fr_state in range(dims[0]):
		for to_state in range(dims[1]):
			if dist((A[fr_state][to_state]), (estA[fr_state][to_state])) > 0.01:
				return False
	return True
	
def bConvTest(B, estB, alphabet):
	dims = B.shape
	for fr_state in range(dims[0]):
		for c in range(dims[1]):
			if dist((B[fr_state][c]), (estB[fr_state][c])) > 0.01:
				return False
	return True
	
def piConvTest(Pi, estPi):
	nStates = len(Pi)
	for state in range(nStates):
		if dist(Pi[state], estPi[state]) > 0.05:
			return False
	return True

def getEst(O, A, B, Pi, alphabet):
	'''
	Maximization step:
	we reestimate our matricies until they converge (to 0.05 points within each other)

	Parameters
	----------
	O: visible observations
	A, B, Pi, alphabet: the parameters of our model 

	Returns
	--------
	A, B, Pi: maximized matricies
	'''
	A1 = getA1(O, A, B, Pi, alphabet)
	B1 = getB1(O, A, B, Pi, alphabet)
	Pi1 = getPi1(O, A, B, Pi, alphabet)
	while (not aConvTest(A, A1) or (not bConvTest(B, B1, alphabet)) or (not piConvTest(Pi, Pi1))):
		A, B, Pi = A1, B1, Pi1
		A, B, Pi = getEst(O, A, B, Pi, alphabet)
	return A, B, Pi

def readCatFile(file):
	'''
	loads in the category data
	'''
	f = open(file)
	text = [line.strip() for line in f.readlines()]
	rv = ''
	for line in text:
		rv += line
	return rv

#given a model M = (A, B, Pi) and a sequence of observations
# O = (01, 02, ... 0N), return the probabilty of witnessing said sequence
def getProbGivenModel(O, A, B, Pi):
	alphabet = getAlphabet(O)
	prob = forward(O, A, B, Pi, alphabet)
	return prob


def genTrainedModel():
	# now we generate a model based on training data, 'categoryData.txt'
	# we will use a 2-state HMM because we think the states will represent "luxury goods" and "nececity goods"
	trainA = genA(2)
	trainPi = genPi(2)


	# we think people prefer to buy more expensive goods in the "luxury prefering state", since luxuries tend to be more expensive
	# since the Baum-Welch algorithm of the HMM produces local, not global, we initialize our emission matrix so one state prefers 
	# more expensive purchases
	trainB = array([(0.02, 0.03, 0.95), (0.1, 0.03, 0.87)])

	#read-in the traning data as our observations, obs
	obs = readCatFile('categoryData.txt')[290:390]
	alphabet = ['l','h','m']

	return getEst(obs, trainA, trainB, trainPi, alphabet)
	
# we test the probablity at 10-purchase intervals, checking to see if 
# the difference between any two purchases 	
def testModel(A, B, Pi):
	a1 = getTotProb(O1, 15, A, B, Pi, ['h', 'm', 'l'])
	a2 = getTotProb(O2, 15, A, B, Pi, ['h', 'm', 'l'])
