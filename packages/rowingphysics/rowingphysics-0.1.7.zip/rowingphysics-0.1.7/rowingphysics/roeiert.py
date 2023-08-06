from math import *
import time
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

from pylab import *


def plotroeiert():
    mhead = 9
    mlegs = 33
    mtrunk = 46
    marms = 11
    xhand = array([5,60,85,130])
    xfoot = array([25,25,25,25])
    xslide = array([75,115,117,120])
    xshoulder = array([55,110,130,145])
    
    mtot = mhead+mlegs+mtrunk+marms

    xcm = 0.5*mlegs*(xslide+xfoot)+0.5*marms*(xshoulder+xhand)
    xcm += mhead*xshoulder+0.5*mtrunk*(xslide+xshoulder)

    xcm /= mtot

    print xcm

    clf()
    subplot(111)
    plot(xhand,xcm,'o-',label='CM')
    plot(xhand,xshoulder,'o-',label='shoulder')
    plot(xhand,xfoot,'o-',label='foot')
    plot(xhand,xslide,'o-',label='slide')
    plot(xhand,xhand,'o-',label='hand')
    legend(loc='best')
    xlabel("x hand")
    ylabel('x')

    show()

def plotroeiert2():
    mhead = 9
    mlegs = 33
    mtrunk = 46
    marms = 11
    xhand = array([5,25,85,130])
    xfoot = array([25,25,25,25])
    xslide = array([75,90,117,120])
    xshoulder = array([55,90,130,145])
    
    mtot = mhead+mlegs+mtrunk+marms

    xcm = 0.5*mlegs*(xslide+xfoot)+0.5*marms*(xshoulder+xhand)
    xcm += mhead*xshoulder+0.5*mtrunk*(xslide+xshoulder)

    xcm /= mtot

    print xcm

    clf()
    subplot(111)
    plot(xhand,xcm,'o-',label='CM')
    plot(xhand,xshoulder,'o-',label='shoulder')
    plot(xhand,xfoot,'o-',label='foot')
    plot(xhand,xslide,'o-',label='slide')
    plot(xhand,xhand,'o-',label='hand')
    legend(loc='best')
    xlabel("x hand")
    ylabel('x')

    show()


def plotroeiert3():
    mhead = 9
    mlegs = 33
    mtrunk = 46
    marms = 11
    xhand = array([5,25,60,85,130])
    xfoot = array([25,25,25,25,25])
    xslide = array([75,90,115,117,120])
    xshoulder = array([55,90,110,130,145])
    
    mtot = mhead+mlegs+mtrunk+marms

    xcm = 0.5*mlegs*(xslide+xfoot)+0.5*marms*(xshoulder+xhand)
    xcm += mhead*xshoulder+0.5*mtrunk*(xslide+xshoulder)

    xcm /= mtot

    print xcm

    print xhand

    clf()
    subplot(111)
    plot(xhand,xcm,'o-',label='CM')
    plot(xhand,xshoulder,'o-',label='shoulder')
    plot(xhand,xfoot,'o-',label='foot')
    plot(xhand,xslide,'o-',label='slide')
    plot(xhand,xhand,'o-',label='hand')
    legend(loc='best')
    xlabel("x hand")
    ylabel('x')

    show()

def plotroeiert4():
    mhead = 9
    mlegs = 33
    mtrunk = 46
    marms = 11
    xhand = (array([-9,-5.5,4,12,19])+9)/28.
    xfoot = (array([0,0,0,0,0])+9)/28.
    xslide = (array([7,12,19,20,22])+9)/28.
    xshoulder = (array([3,9,17,23,26])+9)/28.
    
    mtot = mhead+mlegs+mtrunk+marms

    xcm = 0.5*mlegs*(xslide+xfoot)+0.5*marms*(xshoulder+xhand)
    xcm += mhead*xshoulder+0.5*mtrunk*(xslide+xshoulder)

    xcm /= mtot

    result = polyfit(xhand,xcm,2)
    print result

    xhand2 = linspace(0,1,20)
    xcm2 = result[2]+result[1]*xhand2+result[0]*xhand2**2



    print xcm

    clf()
    subplot(111)
    plot(xhand,xcm,'o-',label='CM')
    plot(xhand,xshoulder,'o-',label='shoulder')
    plot(xhand,xfoot,'o-',label='foot')
    plot(xhand,xslide,'o-',label='slide')
    plot(xhand,xhand,'o-',label='hand')
    plot(xhand2,xcm2,'b-',label='fit')
    legend(loc='best')
    xlabel("x hand")
    ylabel('x')

    show()


def plotroeiert5():
    mhead = 9
    mlegs = 33
    mtrunk = 46
    marms = 11
    xhand = (array([14,13,3,-4,-9])+9)/28.
    xfoot = (array([0,0,0,0,0])+9)/28.
    xslide = (array([16,15,17,11,8])+9)/28.
    xshoulder = (array([20,20,15,8,4])+9)/28.
    
    mtot = mhead+mlegs+mtrunk+marms

    xcm = 0.5*mlegs*(xslide+xfoot)+0.5*marms*(xshoulder+xhand)
    xcm += mhead*xshoulder+0.5*mtrunk*(xslide+xshoulder)

    xcm /= mtot

    result = polyfit(xhand,xcm,2)
    print result

    xhand2 = linspace(0,1,20)
    xcm2 = result[2]+result[1]*xhand2+result[0]*xhand2**2



    print xcm

    clf()
    subplot(111)
    plot(xhand,xcm,'o-',label='CM')
    plot(xhand,xshoulder,'o-',label='shoulder')
    plot(xhand,xfoot,'o-',label='foot')
    plot(xhand,xslide,'o-',label='slide')
    plot(xhand,xhand,'o-',label='hand')
    plot(xhand2,xcm2,'b-',label='fit')
    legend(loc='best')
    xlabel("x hand")
    ylabel('x')

    show()
