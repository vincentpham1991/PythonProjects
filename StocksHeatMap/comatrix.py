import string
import pylab
import itertools
import matplotlib.pyplot as plt
from itertools import combinations
from numpy import array, ndenumerate, arange, empty, transpose, flipud
from matplotlib.widgets import Slider, Button, RadioButtons

class ComatrixPlotter(object):
    SLIDER_START = 0.10
    SLIDER_INCR = -0.05

    def __init__(self, labels, varname, updater, show_numbers = False):
        self.labels = labels
        self.varname = varname
        self.updater = updater
        self.show_numbers = show_numbers
        self.sliders = []
        self.mesh = None

    def update(self, newval):
        self.data = flipud(self.updater(self.get_slider_values()))
        
        self.mesh.set_array(self.data.ravel())

        if self.show_numbers:
            for (x,y),v in ndenumerate(self.data):
                pylab.text(x+0.5,y+0.5,"%.2f"%v)

        pylab.draw()

    def add_slider(self, label, minval, maxval, initval):
        self.sliders.append(ComatrixSlider(label, minval, maxval, initval))

    def get_slider_values(self):
        return [s.get_value() for s in self.sliders]

    def show(self):
        ax = plt.subplot(111)
        plt.subplots_adjust(left=0.25, bottom=0.25)

        self.data = self.updater(self.get_slider_values())
        self.mesh = pylab.pcolormesh(self.data, vmin=-1.0, vmax=1.0)

        self.update(None)

        pylab.colorbar()
        
        ticks = arange(0.5, len(self.labels), 1)
        plt.xticks(ticks, self.labels)
        for tick in pylab.gca().xaxis.iter_ticks():
            tick[0].label2On = True
            tick[0].label1On = False
            tick[0].label2.set_rotation('vertical')

        plt.yticks(ticks, self.labels[::-1])
        plt.xlabel(self.varname + ' 1')
        plt.ylabel(self.varname + ' 2')

        for i, s in enumerate(self.sliders):
            pos = self.SLIDER_START + (i*self.SLIDER_INCR)
            ax = plt.axes([0.25, pos, 0.5, 0.03])
            s.slider = Slider(ax, s.label, s.minval, s.maxval, s.initval)
            s.slider.on_changed(self.update)

        pylab.show()

class ComatrixSlider(object):

    def __init__(self, label, minval, maxval, initval):
        self.label = label
        self.minval = minval
        self.maxval = maxval
        self.initval = initval
        self.slider = None

    def get_value(self):
        if self.slider is None:
            return self.initval
        else:
            return self.slider.val
        

def sample_data_updater(params):
    data = empty([nlabels,nlabels])

    for i in range(nlabels):
        data[i][i]=1.0

    for i,j in combinations(range(nlabels), 2):
        n = abs(i-j)/float(nlabels)
        data[i][j] = n
        data[j][i] = n

    adj = 0.0
    for p in params:
        adj += (p/100.0)

    for i in range(nlabels):
        for j in range(nlabels):
            data[i][j] = min(1.0, data[i][j]+adj)

    print data
    
    return data

if __name__ == "__main__":
    import sys

    nlabels = int(sys.argv[1])
    if nlabels > len(string.ascii_uppercase)**2:
        print "Can't generate more than %i labels" % len(string.ascii_uppercase)**2
        exit(1)
    
    labels = []
    for p in itertools.product(string.ascii_uppercase, repeat=2):
        labels.append("XX" + ''.join(p))
        if len(labels) == nlabels:
            break

    cp = ComatrixPlotter(labels, "Variable", sample_data_updater)
    cp.add_slider("Slider 1", 0, 100, 10)
    cp.add_slider("Slider 2", 0, 10, 0)

    cp.show()

