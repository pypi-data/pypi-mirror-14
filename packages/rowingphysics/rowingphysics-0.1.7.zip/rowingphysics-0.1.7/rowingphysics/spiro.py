#! /usr/bin/python
from math import *
import time
try:
   from pylab import *
except ImportError:
   print "PyLab not available"

from numpy import *
# from srnumerical import *

try:
   from scipy import *
except ImportError:
   print "SciPy not available"

try:
   from matplotlib import *
except ImportError:
   print "Matplotlib not available"

def srcolumn(filename,first=0):

    data = genfromtxt(filename,skip_header=first)

    return array(transpose(data))

def rebin(a, *args):
    '''rebin ndarray data into a smaller ndarray of the same rank whose dimensions
    are factors of the original dimensions. eg. An array with 6 columns and 4 rows
    can be reduced to have 6,3,2 or 1 columns and 4,2 or 1 rows.
    example usages:
    >>> a=rand(6,4); b=rebin(a,3,2)
    >>> a=rand(6); b=rebin(a,2)
    '''
    shape = a.shape
    lenShape = len(shape)
    factor = asarray(shape)/asarray(args)
    evList = ['a.reshape('] + \
             ['args[%d],factor[%d],'%(i,i) for i in range(lenShape)] + \
             [')'] + ['.sum(%d)'%(i+1) for i in range(lenShape)] + \
             ['/factor[%d]'%i for i in range(lenShape)]
#    print ''.join(evList)
    return eval(''.join(evList))

def plotspiro(filename,reb=2,doplot=1):
    data = srcolumn(filename,first=1)
    time = data[0,]
    hr = data[1,]
    vo2 = data[2,]
    vo2_hr = data[4,]
    RER = data[5,]
    VE = data[6,]
    BF = data[9,]

    power = 150.+10*floor(time/30.)
    
    
    aantal = len(time)
    aantal2 = len(time)/reb

    hr = rebin(hr,aantal2)
    power = rebin(power,aantal2)
    vo2 = rebin(vo2,aantal2)
    time = rebin(time,aantal2)
    vo2_hr = rebin(vo2_hr,aantal2)
    RER = rebin(RER,aantal2)
    VE = rebin(VE,aantal2)
    BG = rebin(BF,aantal2)

    if (doplot==1):
       clf()
       ax1 = subplot(111)
       plot(power,vo2,'b.',label='VO2')
       pylab.legend(loc='upper right')
       ylabel("VO2/kg (ml/min/kg)")
       xlabel("power (W)")
       ylabel("HR (bpm)")

       ax2 = twinx()
       plot(power,hr,'ro',label="HR")
       pylab.legend(loc='upper left')
       ax2.yaxis.tick_right()

       show()

    if (doplot==2):

       clf()
       plot(hr,vo2,'ro')
       xlabel("HR (bpm)")
       ylabel("VO2/kg (ml/min/kg)")

       show()

    if (doplot==3):
       clf()
       ax1 = subplot(111)
       plot(time,vo2,'b.',label='VO2')
       pylab.legend(loc='upper left')
       xlabel("time (s)")
       ylabel("VO2 (ml/min/kg)")
       
       ax2 = twinx()
       plot(time,hr,'ro',label='HR')
       pylab.legend(loc='upper right')
       ylabel("HR (bpm)")
       ax2.yaxis.tick_right()

       show()

    if (doplot==4):
       clf()
       ax1 = subplot(111)
       plot(power,RER,'b.',label='RER')
       xlabel("Power (W)")
       ylabel("RER")

       ax2 = twinx()
       plot(power,hr,'ro',label='HR')
       pylab.legend(loc='upper right')
       ylabel("HR (bpm)")
       ax2.yaxis.tick_right()

       show()

    if (doplot==5):
       clf()
       plot(hr,RER,'b.',label='RER')
       xlabel("HR (bpm)")
       ylabel("RER")

       show()
