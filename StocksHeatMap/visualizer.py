import os.path
import sys
import numpy
import comatrix

USAGE = "python visualizer.py stock <data-directory>"

def correlation_matrix(params):
    interval_start = int(params[0])
    interval_length = int(params[1])

    matrix = data.compute_correlation_matrix(dataset, variables, interval_start, interval_length)

    return numpy.array(matrix)


if (len(sys.argv) != 3):
    print USAGE


datatype = sys.argv[1]

if datatype == "stock":
    try:
        import stocks as data
        varname = "Stock"
    except ImportError, ie:
        print "You specified stock data, but stock.py could not be imported."
        exit(3)
elif datatype == "city":
    try:
        import city as data
        varname ="Variable"
    except ImportError, ie:
        print "You specified stock data, but stock.py could not be imported."
        exit(4)
else:
    print USAGE
    print "The data type must be 'stock' or 'city'"


datadir = sys.argv[2]

if not os.path.isdir(datadir):
    print USAGE
    print datadir + " is not a directory."
    exit(1)

variablesfile = datadir + "/variables.txt"

if not os.path.exists(variablesfile):
    print USAGE
    print datadir + " does not contain a variables.txt file"
    exit(2)

variablesfile = open(variablesfile)
variables = variablesfile.read().strip().split()
variablesfile.close()

dataset = data.read_data_from_dir(datadir, variables)

date_length = data.get_number_of_days(dataset)

cp = comatrix.ComatrixPlotter(variables, varname, correlation_matrix)
cp.add_slider("Start date", 0, date_length, 0)
cp.add_slider("Number of days", 0, 30, 7)
cp.show()
