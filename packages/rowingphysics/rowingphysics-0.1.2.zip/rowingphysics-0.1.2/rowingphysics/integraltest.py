#! /usr/bin/python
from math import *

try:
   from pylab import *
except ImportError:
   print "PyLab not available"

from numpy import *
from srnumerical import *

try:
   from scipy import *
except ImportError:
   print "SciPy not available"

try:
   from matplotlib import *
except ImportError:
   print "Matplotlib not available"


def calcint(power):
    aantal = 100
    x = linspace(0,pi,aantal)
    dx = x[1]-x[0]
    y = (sin(x))**(power)
    
    integral = dx*cumsum(y)

    clf()
    ax1 = subplot(111)
    plot(x,y)
    plot(x,integral)
    

    return max(integral)

def calcintcos():
    aantal = 100
    x = linspace(0,pi,aantal)
    dx = x[1]-x[0]
    y = 1-sin(2*x)

    integral = dx*cumsum(y)

    clf()
    ax1 = subplot(111)
    plot(x,y)
    plot(x,integral)
    

    return max(integral)

