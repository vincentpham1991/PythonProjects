#Name: Vincent Pham
# Can complaints predict crime? Can individual stocks predict composite indices?
#

from pylab import *

complaintCols = range(0,7)
crimeCols = [8,9,10,13,14,15,16]
burglaryCol = 9
complaintTotCol = 18
crimeTotCol = 19

djIndexCol = 44
spyCol = 45
stockCols = range(0,djIndexCol)
djCols = range(0,30)
nondjCols = range(30,djIndexCol)

from numpy import ndarray, asarray, matrix, ones, hstack

def tall_and_skinny(A):
    return A.shape[0] > A.shape[1]

def prepend_ones_column(A):
    """
    Add a ones column to the left side of an array/matrix
    Note: This function will not work with a list-of-lists
    """
    ones_col = ones((A.shape[0], 1))
    return hstack((ones_col, A))

def linear_regression(X_input, Y_input):
    """
    Compute linear regression. Finds beta that minimizes
    X*beta - Y
    in a least squared sense.

    Accepts list-of-lists, arrays, or matrices as input type
    Will return an output of the same type as X_input

    Example:
    >>> X = matrix([[5,2], [3,2], [6,2.1], [7, 3]]) # covariates
    >>> Y = [5,2,6,6] # results - note that we can use either matrices or lists
    >>> beta = linear_regression(X, Y)
    >>> print beta
    [[ 1.20104895]
     [ 1.41083916]
     [-1.6958042 ]]
    >>> print prepend_ones_column(X)*beta # Note that the results are close to Y
    [[ 4.86363636]
     [ 2.04195804]
     [ 6.1048951 ]
     [ 5.98951049]]

    """
    # Convert any input into tall and skinny matrices
    X = matrix(X_input)
    Y = matrix(Y_input)
    if not tall_and_skinny(X):
        X = X.T
    if not tall_and_skinny(Y):
        Y = Y.T

    X = prepend_ones_column(X)

    # Do actual computation
    beta = (X.T*X).I * X.T * Y

    # Return type determined by X_input type
    if isinstance(X_input, list):
        return list(beta.flat)
    if isinstance(X_input, matrix):
        return beta
    if isinstance(X_input, ndarray):
        return asarray(beta.flat)
    raise NotImplementedError(
            "Expected input of list, matrix, or array, got %s"%beta.__class__)

def convertIfFloat(v):
    '''
    If v is a floating point string, convert it to a floating point
    number and return the result.  Return v as is, otherwise.
    '''
    try:
        tmp = float(v)
        return tmp
    except ValueError:
        return v


def readFile(filename, type):
    '''
    Read data from the specified file.  Split the lines and convert
    float strings into floats.

    Inputs:
      filename: name of the file to be read
      type: return type ("list", "matrix", or "array")

    Returns:
      (list of strings, 2D list, array, or matrxix of floats)
    '''
    data = [map(convertIfFloat, x.strip().split(",")) for x in open(filename)]

    if type == "list":
        return (data[0], data[1:])
    elif type == "matrix":
        return (data[0], matrix(data[1:]))
    elif type == "array":
        return (data[0], asarray(data[1:]))
    else:
        print "Unknown data type '" + type + "'"
        return (None, None)


def getSubset(data, cols):
    '''
    Extracts a column or set of subsets of the rows from the data
    and returns an object that has the same type as data.

    Inputs:
      data: 2D list, array, or matrix
      cols: integer or list of integers

    Returns:
      1D list, array, or matrix with the specified column if cols is an integer
      2D list, array, or matrix with the specified columns if cols is a list

    Examples:
      >>> getSubset([[0,1,2], [4,5,6], [7,8,9]], 0)
      [0, 4, 7]

      >>> getSubset(asarray([[0,1,2], [4,5,6], [7,8,9]]), 0)
      array([0, 4, 7])

      >>> getSubset(matrix([[0,1,2], [4,5,6], [7,8,9]]), 0)
      matrix([[0, 4, 7]])

      >>> getSubset([[0,1,2], [4,5,6], [7,8,9]], [0,2])
      [[0, 2], [4, 6], [7, 9]]

      >>> getSubset(asarray([[0,1,2], [4,5,6], [7,8,9]]), [0,2])
      array([[0, 2],
             [4, 6],
             [7, 9]])

      >>> getSubset(matrix([[0,1,2], [4,5,6], [7,8,9]]), [0,2])
      matrix([[0, 2],
             [4, 6],
             [7, 9]])

    '''

    rv = asarray(data)[:, cols]
    if isinstance(data, list):
        return rv.tolist()
    elif isinstance(data, matrix):
        return matrix(rv)
    else:
        return rv





######################
#
#  UTILITY FUNCTIONS
#
######################

def plotHelper(f, xs, ys, xl, yl, t, outputFilename):
    '''
    Draw and label a scatter plot.

    Inputs:
    f: figure
    xs: 1D array floats
    ys: 1D array floats
    xl: string
    yl: string
    t: string
    outputFilename: string

    Displays/Outputs:
    plot or file, depending on whether outputFilename is None.

    Returns: nothing
    '''
    scatter(xs, ys)
    xlabel(xl)
    ylabel(yl)
    title(t)
    if outputFilename != None:
        f.savefig(outputFilename)
        close()


def mkModel(Xs, xcols, ys):
    '''
    Create a model to compute ycol given xcols

    NOTE: This function will not work until you implement computeR2()

    Inputs:
      Xs: 2D array of floats
      ys: 1D array floats

    Returns:
       returns a model as len(xcols) x 1 matrix
    '''

    Xs = Xs[:, xcols]
    model = linear_regression(matrix(Xs), matrix(ys))
    r2 = computeR2(model, Xs, ys)
    return (model, r2)


def mkR2Table(Xs, ys):
    '''
    Create a table of R2 values for one-variable models

    NOTE: This function will not work until you implement computeR2()

    Inputs:
      Xs: 2D array of floats
      ys: 1D array floats
    Returns: list of (integer, float) pairs
    '''

    rv = []
    for i in range(0, len(Xs[0])):
        (model, r2) = mkModel(Xs, [i], ys)
        if model != None:
            rv.append((i, r2))
    return rv


def applyModel(model, Xs):
    '''
    Apply the model to the specified values

    Inputs:
      model: model as returned by linear_regression
      Xs: list of lists of floats

    Returns:
      result of applying the model to the data, as an array.
    '''
    Xs = prepend_ones_column(Xs)
    YCALC = asarray(matrix(Xs)*model)[:,0]
    return YCALC



######################
#
#  Required functions
#
######################

def singleVariable(xs, xl, ys, yl, outputFilename):
	beta = linear_regression(xs,ys)
	y = []
	for day in xs:
            y.append(beta[0]+beta[1]*day)
            
	plot(xs,ys,".")
	plot(xs,y)
	xlabel(xl)
	ylabel(yl)
	savefig("./pix/"+outputFilename)
	clf()

def computeR2(model, Xs, ys):
    ssErr = 0
    ssTot = 0
    xbeta = Xs*model[1:]
    if Xs.ndim == 1:
        y = model[0] + model[1]*Xs
    else:
        y = model[0] + xbeta.sum(axis=1)
    n = len(y)
    for i in range(n):
        ssErr = ssErr + (y[i] - ys[i])**2
        ssTot = ssTot + (ys[i] - mean(ys))**2
    R2 = 1 - ssErr/ssTot
    return R2

def computeBestBivariate(Xs, ys):
    if Xs.ndim == 1:
        return "Bivariate model not posible"
    bestR2 = -1
    numXs = len(Xs[0])

    for i in range(numXs):
        for j in range(i+1,numXs):
            twoXs = Xs[:,(i,j)]
            model = linear_regression(twoXs,ys)
            R2 = computeR2(model,twoXs,ys)
            if R2 > bestR2:
                bestR2 = R2
                bestData = [i,j]
                bestModel = model

    return (bestModel, bestData, bestR2)

def discoverKModel(Xs, ys, K):
    R2Table = mkR2Table(Xs,ys)
    R2Table.sort(key=lambda tup:tup[1])
    R2Table.reverse()
    stocks = [row[0] for row in R2Table]
    stocks = stocks[0:K]
    kStocks = Xs[:,stocks]
    model = linear_regression(kStocks,ys)
    R2 = computeR2(model,kStocks,ys)

    return (model,stocks,R2)

def discoverBestModel(Xs, ys, threshold):
    model, stocks, R2 = discoverKModel(Xs,ys,1)
    K = 2
    diff = sys.maxint
    if Xs.ndim == 1:
        xlength = 1
    else:
        xlength = len(Xs[0])
    while(diff > threshold and K <= xlength):
        newModel, newStocks, newR2 = discoverKModel(Xs,ys,K)
        diff = newR2-R2
        model, stocks, R2 = newModel, newStocks, newR2
        K = K + 1

    return (model,stocks,R2)

def genModelTable(trainingXs, trainingYs, testingXs, testingYs):
    l = []
    if trainingXs.ndim == 1:
        xlength = 1
    else:
        xlength = len(trainingXs[0])
    for i in range(xlength):
        K = i + 1
        model, trainingCol, trainingR2 = discoverKModel(trainingXs, trainingYs, K)
        testingR2 = computeR2(model,testingXs[:,trainingCol],testingYs)
        l.append((K, trainingR2, testingR2, trainingCol))

    return l

