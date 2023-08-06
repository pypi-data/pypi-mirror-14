from rowingphysics import *
from crew import *
from rigging import *
import pylab
import time
import rowing

def plot_blade():

   CLmax = 1.0


   a = linspace(-90,90)*pi/180

   C_D = 2*CLmax*sin(a)**2.
   C_L = CLmax*sin(2.*a)


   clf()
   ax1 = subplot(111)

   plot(a,C_D,label='C_D')
   plot(a,C_L,label='C_L')
   legend(loc='best')
   xlabel("Angle of attack (rad)")
   ylabel('Drag Coefficient')
   
   show()
         

def temposeriesvaughan(tempomin,tempomax,F,crew,rigging,aantal=30,timestep=0.03):

   tm = time.time() 

   tempos = linspace(tempomin,tempomax,aantal)
   velocity = zeros(aantal)
   vmin = zeros(aantal)
   vmax = zeros(aantal)
   power = zeros(aantal)
   ratios=zeros(aantal)
   energies=zeros(aantal)

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0)
         dv = res[0]
         vend = res[1]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10)
      velocity[i] = res[2]
      ratios[i] = res[3]
      energies[i] = res[4]
      power[i] = res[5]
      vmax[i] = res[7]
      vmin[i] = res[8]

   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      plot (tempos,velocity)
      plot (tempos,vmin)
      plot (tempos,vmax)
      xlabel("tempo (spm)")
      ylabel('Velocity (m/s)')

      show()
   except NameError:
      print "No plotting today"

   return calctime



def temposeries(tempomin,tempomax,F,crew,rigging,aantal=30,timestep=0.03):
    
   tm = time.time() 

   tempos = linspace(tempomin,tempomax,aantal)
   velocity = zeros(aantal)
   power = zeros(aantal)
   ratios=zeros(aantal)
   energies=zeros(aantal)

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0)
         dv = res[0]
         vend = res[1]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10)
      velocity[i] = res[2]
      ratios[i] = res[3]
      energies[i] = res[4]
      power[i] = res[5]

   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      subplot(221)
      plot (tempos,velocity)
      xlabel("tempo (spm)")
      ylabel('Velocity (m/s)')

      subplot(222)
      plot (tempos,power)
      xlabel("tempo (spm)")
      ylabel('Power (W)')

      subplot(223)
      plot (power,velocity)
      xlabel("Power (W)")
      ylabel('Velocity (m/s)')


      subplot(224)
      plot (tempos,ratios)
      xlabel("tempo (spm)")
      ylabel('Ratio')

      show()
   except NameError:
      print "No plotting today"

   return calctime

def catchangleseries(anglemin,anglemax,F,crew,rigging,aantal=30,timestep=0.03):

   tm = time.time() 

   catchangles = linspace(anglemin,anglemax,aantal)
   velocity = zeros(aantal)
   power = zeros(aantal)
   ratios=zeros(aantal)
   energies=zeros(aantal)

   for i in range(len(catchangles)):
      dv = 1
      vend = 4
      rigging.catchangle = catchangles[i]
      catchacceler = 5

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,
				    timestep,0,catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,
			  timestep,10,catchacceler=catchacceler)
      velocity[i] = res[2]
      ratios[i] = res[3]
      energies[i] = res[4]
      power[i] = res[5]

   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      subplot(221)
      plot (degrees(catchangles),velocity)
      xlabel("catch angle (o)")
      ylabel('Velocity (m/s)')

      subplot(222)
      plot (degrees(catchangles),power)
      xlabel("catch angle (o)")
      ylabel('Power (W)')

      subplot(223)
      plot (power,velocity)
      xlabel("Power (W)")
      ylabel('Velocity (m/s)')


      subplot(224)
      plot (degrees(catchangles),ratios)
      xlabel("catch angle (o)")
      ylabel('Ratio')

      show()
   except NameError:
      print "No plotting today"

   return calctime

def longlegs(rg,doplot=1,v0=3.962):
   from crew import crew,trapezium
   rr = crew(strokeprofile=trapezium(x1=0.1,h2=0.75),tempo=30.)
   res = rowing.energybalance(250,rr,rg,v0,dt=0.01,doplot=doplot)
   return res

def shortlegs(rg,doplot=1,v0=3.997):
   from crew import crew, trapezium
   rr = crew(strokeprofile=trapezium(x1=0.15,x2=0.5,h2=0.9),tempo=30.)
   res = rowing.energybalance(250,rr,rg,v0,dt=0.01,doplot=doplot)
   return res

def plotrecstyle(crew,trecovery,aantal=50,empirical=0):
    time = linspace(0,trecovery,aantal)
    vh = zeros(aantal)
    vcrecovery = zeros(aantal)
    handlepos = zeros(aantal)+crew.strokelength
    vavg = crew.strokelength/trecovery
    d = crew.strokelength

    for i in range(0,aantal-1):
	vh[i] = crew.vhandle(vavg,trecovery,time[i])
	vcrecovery[i] = crew.vcm(vh[i],handlepos[i])
	handlepos[i+1] = d+d*crew.dxhandle(vavg,trecovery,time[i])

    vh[aantal-1] = crew.vhandle(vavg,trecovery,time[aantal-1])
    vcrecovery[aantal-1] = crew.vcm(vh[aantal-1],handlepos[aantal-1])
			     

    if (empirical<>0):
       empdata = genfromtxt(empirical, delimiter = ',')
       emptime = empdata[:,0]
       empv = -empdata[:,1]
       empdt = emptime[1]-emptime[0]



    clf()
    subplot(211)
    plot(time,vh,'r-',label = 'Handle speed')
    plot(time,vcrecovery, 'b-',label = 'CM speed')
    if (empirical<>0):
	plot(emptime,empv,'g-',label = 'Measured')
    legend(loc='lower right')
    xlabel("time (s)")
    ylabel("velocity (m/s)")


    subplot(212)
    plot(time,handlepos,'r-',label = 'Handle Position')
    legend(loc='upper right')
    xlabel("time (s)")
    ylabel("position (m)")
    show()

def plotrowerforcecurve(F,cr,aantal=50):
    x = linspace(0,cr.strokelength,aantal)
    y1 = zeros(aantal)

    for i in range(len(x)):
	y1[i] = cr.forceprofile(F,x[i])

    clf()
    plot(x,y1,'-g', label='Force Curve')
    legend(loc='best')
    xlabel("Handle Position")
    ylabel('Force')
    show()

    return 1

def plotforcecurve(F,cr,aantal=50):
   from crew import flat,strongmiddle,strongend,strongbegin,trapezium
   
   x = linspace(0,cr.strokelength,aantal)
   y1 = zeros(aantal)
   y2 = zeros(aantal)
   y3 = zeros(aantal)
   y4 = zeros(aantal)
   y5 = zeros(aantal)

   cr.strokeprofile = trapezium(x1=0.1,h2=0.5)

   for i in range(len(x)):
      y1[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = trapezium(x1=0.1,h2=0.75)

   for i in range(len(x)):
      y2[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = trapezium(x1=0.1,x2=0.5,h2=0.75)

   for i in range(len(x)):
      y3[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = trapezium(x1=0.15,x2=0.5,h2=0.9)

   for i in range(len(x)):
      y4[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = trapezium()

   for i in range(len(x)):
      y5[i] = cr.forceprofile(F,x[i])


   clf()
   plot(x,y1,'-g', label='T1')
   plot(x,y2,'-r', label='T2')
   plot(x,y3,'-b', label='T3')
   plot(x,y4,'-k', label='T4')
   plot(x,y5,'-m', label='T5')
   legend(loc='best')
   xlabel("Handle Position")
   ylabel('Force')
   show()

   return 1

def plotforcecurveRIM(F,cr,aantal=50):
   from crew import flat,strongmiddle,strongmiddle2,strongend,strongbegin,trapezium
   
   x = linspace(0,cr.strokelength,aantal)
   y1 = zeros(aantal)
   y2 = zeros(aantal)
   y3 = zeros(aantal)
   y4 = zeros(aantal)
   y5 = zeros(aantal)

   cr.strokeprofile = strongmiddle2(frac=-0.5)

   for i in range(len(x)):
      y1[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = strongmiddle2(frac=0)

   for i in range(len(x)):
      y2[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = strongmiddle2(frac=0.5)

   for i in range(len(x)):
      y3[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = strongmiddle2(frac=1)

   for i in range(len(x)):
      y4[i] = cr.forceprofile(F,x[i])

   cr.strokeprofile = trapezium()

   for i in range(len(x)):
      y5[i] = cr.forceprofile(F,x[i])


   clf()
   plot(x,y1,'-g', label='T1')
   plot(x,y2,'-r', label='T2')
   plot(x,y3,'-b', label='T3')
   plot(x,y4,'-k', label='T4')
   plot(x,y5,'-m', label='T5')
   legend(loc='best')
   xlabel("Handle Position")
   ylabel('Force')
   show()

   return 1

def styleseries(tempomin,tempomax,F,crew,rigging,aantal=30,timestep=0.03,doplot=1,timewise=0):

   from crew import flat,strongmiddle,strongend,strongbegin,trapezium
   tm = time.time() 

   tempos = linspace(tempomin,tempomax,aantal)
   velocity1 = zeros(aantal)
   power1 = zeros(aantal)
   ratios1=zeros(aantal)
   energies1=zeros(aantal)
   check1=zeros(aantal)
   RIM_check1 = zeros(aantal)
   RIM_E1 = zeros(aantal)

   crew.strokeprofile = trapezium(x1=0.1,h2=0.5) # flat()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
	 print catchacceler
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity1[i] = res[2]
      ratios1[i] = res[3]
      energies1[i] = res[4]
      power1[i] = res[5]
      check1[i] = res[9]
      RIM_check1[i] = res[11]
      RIM_E1[i] = res[10]

   velocity2 = zeros(aantal)
   power2 = zeros(aantal)
   ratios2=zeros(aantal)
   energies2=zeros(aantal)
   check2=zeros(aantal)
   RIM_check2 = zeros(aantal)
   RIM_E2 = zeros(aantal)

   crew.strokeprofile = trapezium(x1=0.1,h2=0.75) # strongbegin()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity2[i] = res[2]
      ratios2[i] = res[3]
      energies2[i] = res[4]
      power2[i] = res[5]
      check2[i] = res[9]
      RIM_check2[i] = res[11]
      RIM_E2[i] = res[10]

   velocity3 = zeros(aantal)
   power3 = zeros(aantal)
   ratios3=zeros(aantal)
   energies3=zeros(aantal)
   check3=zeros(aantal)
   RIM_check3 = zeros(aantal)
   RIM_E3 = zeros(aantal)

   crew.strokeprofile = trapezium(x1=0.1,x2=0.5,h2=0.75) # strongend()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity3[i] = res[2]
      ratios3[i] = res[3]
      energies3[i] = res[4]
      power3[i] = res[5]
      check3[i] = res[9]
      RIM_check3[i] = res[11]
      RIM_E3[i] = res[10]

   velocity4 = zeros(aantal)
   power4 = zeros(aantal)
   ratios4=zeros(aantal)
   energies4=zeros(aantal)
   check4=zeros(aantal)
   RIM_check4=zeros(aantal)
   RIM_E4=zeros(aantal)

   crew.strokeprofile =  trapezium(x1=0.15,x2=0.5,h2=0.9)  # trapezium()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity4[i] = res[2]
      ratios4[i] = res[3]
      energies4[i] = res[4]
      power4[i] = res[5]
      check4[i] = res[9]
      RIM_check4[i] = res[11]
      RIM_E4[i] = res[10]


   velocity5 = zeros(aantal)
   power5 = zeros(aantal)
   ratios5=zeros(aantal)
   energies5=zeros(aantal)
   check5=zeros(aantal)
   RIM_check5 = zeros(aantal)
   RIM_E5 = zeros(aantal)

   crew.strokeprofile = trapezium()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity5[i] = res[2]
      ratios5[i] = res[3]
      energies5[i] = res[4]
      power5[i] = res[5]
      check5[i] = res[9]
      RIM_check5[i] = res[11]
      RIM_E5[i] = res[10]



   calctime = time.time()-tm

   [min1,sec1] = rowing.vavgto500mtime(velocity1)
   [min2,sec2] = rowing.vavgto500mtime(velocity2)
   [min3,sec3] = rowing.vavgto500mtime(velocity3)
   [min4,sec4] = rowing.vavgto500mtime(velocity4)
   [min5,sec5] = rowing.vavgto500mtime(velocity5)

   sec1 = sec1+(min1-1)*60.
   sec2 = sec2+(min2-1)*60.
   sec3 = sec3+(min3-1)*60.
   sec4 = sec4+(min4-1)*60.
   sec5 = sec5+(min5-1)*60.

   # plotjes
   try:
      clf()

      if (doplot == 1):
	  plot (power1,velocity1,'go',label='T1 ')
	  plot (power2,velocity2,'rs',label='T2 ')
	  plot (power3,velocity3,'bv',label='T3 ')
	  plot (power4,velocity4,'k^',label='T4 ')
	  plot (power5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('Velocity (m/s)')

      if (doplot == 2):
	  plot (tempos,velocity1,'-g',label='T1')
	  plot (tempos,velocity2,'-r',label='T2')
	  plot (tempos,velocity3,'-b',label='T3')
	  plot (tempos,velocity4,'-k',label='T4')
	  plot (tempos,velocity5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Velocity (m/s)')

      if (doplot == 3):
	  plot (tempos,power1,'-g',label='T1')
	  plot (tempos,power2,'-r',label='T2')
	  plot (tempos,power3,'-b',label='T3')
	  plot (tempos,power4,'-k',label='T4')
	  plot (tempos,power5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Power (W)')

      if (doplot == 4):

	  plot (power1,sec1,'-g',label='T1')
	  plot (power2,sec2,'-r',label='T2')
	  plot (power4,sec3,'-b',label='T3')
	  plot (power3,sec4,'-k',label='T4')
	  plot (power3,sec5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('500m time')

      if (doplot == 5):
	  plot (check1,velocity1,'go',label='T1 ')
	  plot (check2,velocity2,'rs',label='T2 ')
	  plot (check3,velocity3,'bv',label='T3 ')
	  plot (check4,velocity4,'k^',label='T4 ')
	  plot (check5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Check (m2/s4)")
	  ylabel('Velocity (m/s)')

      if (doplot == 6):
	  plot (tempos,check1,'go',label='T1')
	  plot (tempos,check2,'rs',label='T2')
	  plot (tempos,check3,'bv',label='T3')
	  plot (tempos,check4,'k^',label='T4')
	  plot (tempos,check5,'mo',label='T5')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Crewnerd Check (m2/s4)')

      if (doplot == 7):
	  plot (RIM_check1,velocity1,'-go',label='T1')
	  plot (RIM_check2,velocity2,'-rs',label='T2')
	  plot (RIM_check3,velocity3,'-bv',label='T3')
	  plot (RIM_check4,velocity4,'-k^',label='T4')
	  plot (RIM_check5,velocity5,'-mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Check (m/s)')

      if (doplot == 8):
	  plot (RIM_E1,velocity1,'go',label='T1')
	  plot (RIM_E2,velocity2,'rs',label='T2')
	  plot (RIM_E3,velocity3,'bv',label='T3')
	  plot (RIM_E4,velocity4,'k^',label='T4')
	  plot (RIM_E5,velocity5,'mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Stroke Efficiency (m)')



      show()
   except NameError:
      print "No plotting today"

   return calctime


def catchseriesRIM(anglemin,anglemax,F,crew,rigging,aantal=30,timestep=0.03,doplot=1,timewise=0):

   from crew import flat,strongmiddle,strongmiddle2,strongend,strongbegin,trapezium
   tm = time.time() 

   catchangles = linspace(anglemin,anglemax,aantal)
   velocity1 = zeros(aantal)
   power1 = zeros(aantal)
   ratios1=zeros(aantal)
   energies1=zeros(aantal)
   check1=zeros(aantal)
   RIM_check1 = zeros(aantal)
   RIM_E1 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=-0.5) # fitted

   for i in range(len(catchangles)):
      dv = 1
      vend = 4
      rigging.catchangle = catchangles[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
	 print catchacceler
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity1[i] = res[2]
      ratios1[i] = res[3]
      energies1[i] = res[4]
      power1[i] = res[5]
      check1[i] = res[9]
      RIM_check1[i] = res[11]
      RIM_E1[i] = res[10]

   velocity2 = zeros(aantal)
   power2 = zeros(aantal)
   ratios2=zeros(aantal)
   energies2=zeros(aantal)
   check2=zeros(aantal)
   RIM_check2 = zeros(aantal)
   RIM_E2 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=0) # fitted

   for i in range(len(catchangles)):
      dv = 1
      vend = 4
      rigging.catchangle = catchangles[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity2[i] = res[2]
      ratios2[i] = res[3]
      energies2[i] = res[4]
      power2[i] = res[5]
      check2[i] = res[9]
      RIM_check2[i] = res[11]
      RIM_E2[i] = res[10]

   velocity3 = zeros(aantal)
   power3 = zeros(aantal)
   ratios3=zeros(aantal)
   energies3=zeros(aantal)
   check3=zeros(aantal)
   RIM_check3 = zeros(aantal)
   RIM_E3 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=0.5) # fitted

   for i in range(len(catchangles)):
      dv = 1
      vend = 4
      rigging.catchangle = catchangles[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity3[i] = res[2]
      ratios3[i] = res[3]
      energies3[i] = res[4]
      power3[i] = res[5]
      check3[i] = res[9]
      RIM_check3[i] = res[11]
      RIM_E3[i] = res[10]

   velocity4 = zeros(aantal)
   power4 = zeros(aantal)
   ratios4=zeros(aantal)
   energies4=zeros(aantal)
   check4=zeros(aantal)
   RIM_check4=zeros(aantal)
   RIM_E4=zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=1.0) # fitted

   for i in range(len(catchangles)):
      dv = 1
      vend = 4
      rigging.catchangle = catchangles[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity4[i] = res[2]
      ratios4[i] = res[3]
      energies4[i] = res[4]
      power4[i] = res[5]
      check4[i] = res[9]
      RIM_check4[i] = res[11]
      RIM_E4[i] = res[10]


   velocity5 = zeros(aantal)
   power5 = zeros(aantal)
   ratios5=zeros(aantal)
   energies5=zeros(aantal)
   check5=zeros(aantal)
   RIM_check5 = zeros(aantal)
   RIM_E5 = zeros(aantal)

   crew.strokeprofile = trapezium()

   for i in range(len(catchangles)):
      dv = 1
      vend = 4
      rigging.catchangle = catchangles[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity5[i] = res[2]
      ratios5[i] = res[3]
      energies5[i] = res[4]
      power5[i] = res[5]
      check5[i] = res[9]
      RIM_check5[i] = res[11]
      RIM_E5[i] = res[10]



   calctime = time.time()-tm

   [min1,sec1] = rowing.vavgto500mtime(velocity1)
   [min2,sec2] = rowing.vavgto500mtime(velocity2)
   [min3,sec3] = rowing.vavgto500mtime(velocity3)
   [min4,sec4] = rowing.vavgto500mtime(velocity4)
   [min5,sec5] = rowing.vavgto500mtime(velocity5)

   sec1 = sec1+(min1-1)*60.
   sec2 = sec2+(min2-1)*60.
   sec3 = sec3+(min3-1)*60.
   sec4 = sec4+(min4-1)*60.
   sec5 = sec5+(min5-1)*60.

   catchangles = 180*catchangles/pi

   # plotjes
   try:
      clf()

      if (doplot == 1):
	  plot (power1,velocity1,'go',label='T1 ')
	  plot (power2,velocity2,'rs',label='T2 ')
	  plot (power3,velocity3,'bv',label='T3 ')
	  plot (power4,velocity4,'k^',label='T4 ')
	  plot (power5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('Velocity (m/s)')

      if (doplot == 2):
	  plot (catchangles,velocity1,'-g',label='T1')
	  plot (catchangles,velocity2,'-r',label='T2')
	  plot (catchangles,velocity3,'-b',label='T3')
	  plot (catchangles,velocity4,'-k',label='T4')
	  plot (catchangles,velocity5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("angle (spm)")
	  ylabel('Velocity (m/s)')

      if (doplot == 3):
	  plot (catchangles,power1,'-g',label='T1')
	  plot (catchangles,power2,'-r',label='T2')
	  plot (catchangles,power3,'-b',label='T3')
	  plot (catchangles,power4,'-k',label='T4')
	  plot (catchangles,power5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("angle (spm)")
	  ylabel('Power (W)')

      if (doplot == 4):

	  plot (power1,sec1,'-g',label='T1')
	  plot (power2,sec2,'-r',label='T2')
	  plot (power4,sec3,'-b',label='T3')
	  plot (power3,sec4,'-k',label='T4')
	  plot (power3,sec5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('500m time')

      if (doplot == 5):
	  plot (check1,velocity1,'go',label='T1 ')
	  plot (check2,velocity2,'rs',label='T2 ')
	  plot (check3,velocity3,'bv',label='T3 ')
	  plot (check4,velocity4,'k^',label='T4 ')
	  plot (check5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Check (m2/s4)")
	  ylabel('Velocity (m/s)')

      if (doplot == 6):
	  plot (catchangles,check1,'go',label='T1')
	  plot (catchangles,check2,'rs',label='T2')
	  plot (catchangles,check3,'bv',label='T3')
	  plot (catchangles,check4,'k^',label='T4')
	  plot (catchangles,check5,'mo',label='T5')
	  legend(loc='best')
	  xlabel("angle (spm)")
	  ylabel('Crewnerd Check (m2/s4)')

      if (doplot == 7):
	  plot (RIM_check1,velocity1,'-go',label='T1')
	  plot (RIM_check2,velocity2,'-rs',label='T2')
	  plot (RIM_check3,velocity3,'-bv',label='T3')
	  plot (RIM_check4,velocity4,'-k^',label='T4')
	  plot (RIM_check5,velocity5,'-mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Check (m/s)')

      if (doplot == 8):
	  plot (RIM_E1,velocity1,'go',label='T1')
	  plot (RIM_E2,velocity2,'rs',label='T2')
	  plot (RIM_E3,velocity3,'bv',label='T3')
	  plot (RIM_E4,velocity4,'k^',label='T4')
	  plot (RIM_E5,velocity5,'mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Stroke Efficiency (m)')



      show()
   except NameError:
      print "No plotting today"

   return calctime

def styleseriesRIM(tempomin,tempomax,F,crew,rigging,aantal=30,timestep=0.03,doplot=1,timewise=0):

   from crew import flat,strongmiddle,strongmiddle2,strongend,strongbegin,trapezium
   tm = time.time() 

   tempos = linspace(tempomin,tempomax,aantal)
   velocity1 = zeros(aantal)
   power1 = zeros(aantal)
   ratios1=zeros(aantal)
   energies1=zeros(aantal)
   check1=zeros(aantal)
   RIM_check1 = zeros(aantal)
   RIM_E1 = zeros(aantal)
   efficiencies1 = zeros(aantal)
   RIM_effs1 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=-0.5) # fitted

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
	 print catchacceler
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity1[i] = res[2]
      ratios1[i] = res[3]
      energies1[i] = res[4]
      power1[i] = res[5]
      efficiencies1[i] = res[6]
      RIM_effs1[i] = res[15]
      check1[i] = res[9]
      RIM_check1[i] = res[11]
      RIM_E1[i] = res[10]

   velocity2 = zeros(aantal)
   power2 = zeros(aantal)
   ratios2=zeros(aantal)
   energies2=zeros(aantal)
   check2=zeros(aantal)
   RIM_check2 = zeros(aantal)
   RIM_E2 = zeros(aantal)
   efficiencies2 = zeros(aantal)
   RIM_effs2 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=0) # fitted

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity2[i] = res[2]
      ratios2[i] = res[3]
      energies2[i] = res[4]
      power2[i] = res[5]
      efficiencies2[i] = res[6]
      RIM_effs2[i] = res[15]
      check2[i] = res[9]
      RIM_check2[i] = res[11]
      RIM_E2[i] = res[10]
#      print tempos[i],power2[i],velocity2[i],RIM_effs2[i]

   velocity3 = zeros(aantal)
   power3 = zeros(aantal)
   ratios3=zeros(aantal)
   energies3=zeros(aantal)
   check3=zeros(aantal)
   RIM_check3 = zeros(aantal)
   RIM_E3 = zeros(aantal)
   efficiencies3 = zeros(aantal)
   RIM_effs3 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=0.5) # fitted

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity3[i] = res[2]
      ratios3[i] = res[3]
      energies3[i] = res[4]
      power3[i] = res[5]
      efficiencies3[i] = res[6]
      RIM_effs3[i] = res[15]
      check3[i] = res[9]
      RIM_check3[i] = res[11]
      RIM_E3[i] = res[10]
#      print tempos[i],power3[i],velocity3[i],RIM_effs3[i]

   velocity4 = zeros(aantal)
   power4 = zeros(aantal)
   ratios4=zeros(aantal)
   energies4=zeros(aantal)
   check4=zeros(aantal)
   RIM_check4=zeros(aantal)
   RIM_E4=zeros(aantal)
   efficiencies4 = zeros(aantal)
   RIM_effs4 = zeros(aantal)

   crew.strokeprofile = strongmiddle2(frac=1.0) # fitted

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity4[i] = res[2]
      ratios4[i] = res[3]
      energies4[i] = res[4]
      power4[i] = res[5]
      efficiencies4[i] = res[6]
      RIM_effs4[i] = res[15]
      check4[i] = res[9]
      RIM_check4[i] = res[11]
      RIM_E4[i] = res[10]


   velocity5 = zeros(aantal)
   power5 = zeros(aantal)
   ratios5=zeros(aantal)
   energies5=zeros(aantal)
   check5=zeros(aantal)
   RIM_check5 = zeros(aantal)
   RIM_E5 = zeros(aantal)
   efficiencies5 = zeros(aantal)
   RIM_effs5 = zeros(aantal)

   crew.strokeprofile = trapezium()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity5[i] = res[2]
      ratios5[i] = res[3]
      energies5[i] = res[4]
      power5[i] = res[5]
      efficiencies5[i] = res[6]
      RIM_effs5[i] = res[15]
      check5[i] = res[9]
      RIM_check5[i] = res[11]
      RIM_E5[i] = res[10]



   calctime = time.time()-tm

   [min1,sec1] = rowing.vavgto500mtime(velocity1)
   [min2,sec2] = rowing.vavgto500mtime(velocity2)
   [min3,sec3] = rowing.vavgto500mtime(velocity3)
   [min4,sec4] = rowing.vavgto500mtime(velocity4)
   [min5,sec5] = rowing.vavgto500mtime(velocity5)

   sec1 = sec1+(min1-1)*60.
   sec2 = sec2+(min2-1)*60.
   sec3 = sec3+(min3-1)*60.
   sec4 = sec4+(min4-1)*60.
   sec5 = sec5+(min5-1)*60.

   # plotjes
   try:
      clf()

      if (doplot == 1):
	  plot (power1,velocity1,'go',label='T1 ')
	  plot (power2,velocity2,'rs',label='T2 ')
	  plot (power3,velocity3,'bv',label='T3 ')
	  plot (power4,velocity4,'k^',label='T4 ')
	  plot (power5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('Velocity (m/s)')

      if (doplot == 2):
	  plot (tempos,velocity1,'-g',label='T1')
	  plot (tempos,velocity2,'-r',label='T2')
	  plot (tempos,velocity3,'-b',label='T3')
	  plot (tempos,velocity4,'-k',label='T4')
	  plot (tempos,velocity5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Velocity (m/s)')

      if (doplot == 3):
	  plot (tempos,power1,'-g',label='T1')
	  plot (tempos,power2,'-r',label='T2')
	  plot (tempos,power3,'-b',label='T3')
	  plot (tempos,power4,'-k',label='T4')
	  plot (tempos,power5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Power (W)')

      if (doplot == 4):

	  plot (power1,sec1,'-g',label='T1')
	  plot (power2,sec2,'-r',label='T2')
	  plot (power4,sec3,'-b',label='T3')
	  plot (power3,sec4,'-k',label='T4')
	  plot (power3,sec5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('500m time')

      if (doplot == 5):
	  plot (check1,velocity1,'go',label='T1 ')
	  plot (check2,velocity2,'rs',label='T2 ')
	  plot (check3,velocity3,'bv',label='T3 ')
	  plot (check4,velocity4,'k^',label='T4 ')
	  plot (check5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Check (m2/s4)")
	  ylabel('Velocity (m/s)')

      if (doplot == 6):
	  plot (tempos,check1,'go',label='T1')
	  plot (tempos,check2,'rs',label='T2')
	  plot (tempos,check3,'bv',label='T3')
	  plot (tempos,check4,'k^',label='T4')
	  plot (tempos,check5,'mo',label='T5')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Crewnerd Check (m2/s4)')

      if (doplot == 7):
	  plot (RIM_check1,velocity1,'-go',label='T1')
	  plot (RIM_check2,velocity2,'-rs',label='T2')
	  plot (RIM_check3,velocity3,'-bv',label='T3')
	  plot (RIM_check4,velocity4,'-k^',label='T4')
	  plot (RIM_check5,velocity5,'-mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Check (m/s)')

      if (doplot == 8):
	  plot (RIM_E1,velocity1,'go',label='T1')
	  plot (RIM_E2,velocity2,'rs',label='T2')
	  plot (RIM_E3,velocity3,'bv',label='T3')
	  plot (RIM_E4,velocity4,'k^',label='T4')
	  plot (RIM_E5,velocity5,'mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Stroke Efficiency (m)')

      if (doplot == 9):
	  plot (RIM_effs1,velocity1,'go',label='T1')
	  plot (RIM_effs2,velocity2,'rs',label='T2')
	  plot (RIM_effs3,velocity3,'bv',label='T3')
	  plot (RIM_effs4,velocity4,'k^',label='T4')
	  plot (RIM_effs5,velocity5,'mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('Fluid Drag Efficiency')

      if (doplot == 10):
	  plot (efficiencies1,velocity1,'go',label='T1')
	  plot (efficiencies2,velocity2,'rs',label='T2')
	  plot (efficiencies3,velocity3,'bv',label='T3')
	  plot (efficiencies4,velocity4,'k^',label='T4')
	  plot (efficiencies5,velocity5,'mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('Efficiency')



      show()
   except NameError:
      print "No plotting today"

   return calctime


def styleseriesforce(Fmin,Fmax,crew,rigging,aantal=30,timestep=0.03,doplot=1,timewise=0):

   from crew import flat,strongmiddle,strongend,strongbegin,trapezium
   tm = time.time() 

   Forces = linspace(Fmin,Fmax,aantal)
   velocity1 = zeros(aantal)
   power1 = zeros(aantal)
   ratios1=zeros(aantal)
   energies1=zeros(aantal)
   check1=zeros(aantal)
   RIM_check1 = zeros(aantal)
   RIM_E1 = zeros(aantal)

   crew.strokeprofile = trapezium(x1=0.1,h2=0.5) # flat()

   for i in range(len(Forces)):
      dv = 1
      vend = 4
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity1[i] = res[2]
      ratios1[i] = res[3]
      energies1[i] = res[4]
      power1[i] = res[5]
      check1[i] = res[9]
      RIM_check1[i] = res[11]
      RIM_E1[i] = res[10]

   velocity2 = zeros(aantal)
   power2 = zeros(aantal)
   ratios2=zeros(aantal)
   energies2=zeros(aantal)
   check2=zeros(aantal)
   RIM_check2 = zeros(aantal)
   RIM_E2 = zeros(aantal)

   crew.strokeprofile = trapezium(x1=0.1,h2=0.75) # strongbegin()

   for i in range(len(Forces)):
      dv = 1
      vend = 4
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity2[i] = res[2]
      ratios2[i] = res[3]
      energies2[i] = res[4]
      power2[i] = res[5]
      check2[i] = res[9]
      RIM_check2[i] = res[11]
      RIM_E2[i] = res[10]

   velocity3 = zeros(aantal)
   power3 = zeros(aantal)
   ratios3=zeros(aantal)
   energies3=zeros(aantal)
   check3=zeros(aantal)
   RIM_check3 = zeros(aantal)
   RIM_E3 = zeros(aantal)

   crew.strokeprofile = trapezium(x1=0.1,x2=0.5,h2=0.75) # strongend()

   for i in range(len(Forces)):
      dv = 1
      vend = 4
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity3[i] = res[2]
      ratios3[i] = res[3]
      energies3[i] = res[4]
      power3[i] = res[5]
      check3[i] = res[9]
      RIM_check3[i] = res[11]
      RIM_E3[i] = res[10]

   velocity4 = zeros(aantal)
   power4 = zeros(aantal)
   ratios4=zeros(aantal)
   energies4=zeros(aantal)
   check4=zeros(aantal)
   RIM_check4=zeros(aantal)
   RIM_E4=zeros(aantal)

   crew.strokeprofile =  trapezium(x1=0.15,x2=0.5,h2=0.9)  # trapezium()

   for i in range(len(Forces)):
      dv = 1
      vend = 4
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity4[i] = res[2]
      ratios4[i] = res[3]
      energies4[i] = res[4]
      power4[i] = res[5]
      check4[i] = res[9]
      RIM_check4[i] = res[11]
      RIM_E4[i] = res[10]


   velocity5 = zeros(aantal)
   power5 = zeros(aantal)
   ratios5=zeros(aantal)
   energies5=zeros(aantal)
   check5=zeros(aantal)
   RIM_check5 = zeros(aantal)
   RIM_E5 = zeros(aantal)

   crew.strokeprofile = trapezium()

   for i in range(len(Forces)):
      dv = 1
      vend = 4
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity5[i] = res[2]
      ratios5[i] = res[3]
      energies5[i] = res[4]
      power5[i] = res[5]
      check5[i] = res[9]
      RIM_check5[i] = res[11]
      RIM_E5[i] = res[10]



   calctime = time.time()-tm

   [min1,sec1] = rowing.vavgto500mtime(velocity1)
   [min2,sec2] = rowing.vavgto500mtime(velocity2)
   [min3,sec3] = rowing.vavgto500mtime(velocity3)
   [min4,sec4] = rowing.vavgto500mtime(velocity4)
   [min5,sec5] = rowing.vavgto500mtime(velocity5)

   sec1 = sec1+(min1-1)*60.
   sec2 = sec2+(min2-1)*60.
   sec3 = sec3+(min3-1)*60.
   sec4 = sec4+(min4-1)*60.
   sec5 = sec5+(min5-1)*60.

   # plotjes
   try:
      clf()

      if (doplot == 1):
	  plot (power1,velocity1,'go',label='T1 ')
	  plot (power2,velocity2,'rs',label='T2 ')
	  plot (power3,velocity3,'bv',label='T3 ')
	  plot (power4,velocity4,'k^',label='T4 ')
	  plot (power5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('Velocity (m/s)')

      if (doplot == 2):
	  plot (Forces,velocity1,'-g',label='T1')
	  plot (Forces,velocity2,'-r',label='T2')
	  plot (Forces,velocity3,'-b',label='T3')
	  plot (Forces,velocity4,'-k',label='T4')
	  plot (Forces,velocity5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("Force (N)")
	  ylabel('Velocity (m/s)')

      if (doplot == 3):
	  plot (Forces,power1,'-g',label='T1')
	  plot (Forces,power2,'-r',label='T2')
	  plot (Forces,power3,'-b',label='T3')
	  plot (Forces,power4,'-k',label='T4')
	  plot (Forces,power5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("Force (N)")
	  ylabel('Power (W)')

      if (doplot == 4):

	  plot (power1,sec1,'-g',label='T1')
	  plot (power2,sec2,'-r',label='T2')
	  plot (power4,sec3,'-b',label='T3')
	  plot (power3,sec4,'-k',label='T4')
	  plot (power3,sec5,'-m',label='T5')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('500m time')

      if (doplot == 5):
	  plot (check1,velocity1,'go',label='T1 ')
	  plot (check2,velocity2,'rs',label='T2 ')
	  plot (check3,velocity3,'bv',label='T3 ')
	  plot (check4,velocity4,'k^',label='T4 ')
	  plot (check5,velocity5,'mo',label='T5 ')
	  legend(loc='best')
	  xlabel("Check (m2/s4)")
	  ylabel('Velocity (m/s)')

      if (doplot == 6):
	  plot (Forces,check1,'go',label='T1')
	  plot (Forces,check2,'rs',label='T2')
	  plot (Forces,check3,'bv',label='T3')
	  plot (Forces,check4,'k^',label='T4')
	  plot (Forces,check5,'mo',label='T5')
	  legend(loc='best')
	  xlabel("Force (N)")
	  ylabel('Crewnerd Check (m2/s4)')

      if (doplot == 7):
	  plot (RIM_check1,velocity1,'-go',label='T1')
	  plot (RIM_check2,velocity2,'-rs',label='T2')
	  plot (RIM_check3,velocity3,'-bv',label='T3')
	  plot (RIM_check4,velocity4,'-k^',label='T4')
	  plot (RIM_check5,velocity5,'-mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Check (m/s)')

      if (doplot == 8):
	  plot (RIM_E1,velocity1,'go',label='T1')
	  plot (RIM_E2,velocity2,'rs',label='T2')
	  plot (RIM_E3,velocity3,'bv',label='T3')
	  plot (RIM_E4,velocity4,'k^',label='T4')
	  plot (RIM_E5,velocity5,'mo',label='T5')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Stroke Efficiency (m)')



      show()
   except NameError:
      print "No plotting today"

   return calctime

def recoverystyleseries(tempomin,tempomax,F,crew,rigging,aantal=30,timestep=0.03,doplot=1,timewise=0):

   from crew import flatrecovery,sinusrecovery,trianglerecovery,realisticrecovery
   tm = time.time() 

   tempos = linspace(tempomin,tempomax,aantal)
   velocity1 = zeros(aantal)
   power1 = zeros(aantal)
   ratios1=zeros(aantal)
   energies1=zeros(aantal)
   check1=zeros(aantal)
   RIM_check1 = zeros(aantal)
   RIM_E1 = zeros(aantal)

   crew.recprofile = flatrecovery()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity1[i] = res[2]
      ratios1[i] = res[3]
      energies1[i] = res[4]
      power1[i] = res[5]
      check1[i] = res[9]
      RIM_check1[i] = res[11]
      RIM_E1[i] = res[10]
      
   velocity2 = zeros(aantal)
   power2 = zeros(aantal)
   ratios2=zeros(aantal)
   energies2=zeros(aantal)
   check2=zeros(aantal)
   RIM_check2 = zeros(aantal)
   RIM_E2 = zeros(aantal)

   crew.recprofile = sinusrecovery()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity2[i] = res[2]
      ratios2[i] = res[3]
      energies2[i] = res[4]
      power2[i] = res[5]
      check2[i] = res[9]
      RIM_check2[i] = res[11]
      RIM_E2[i] = res[10]

   velocity3 = zeros(aantal)
   power3 = zeros(aantal)
   ratios3=zeros(aantal)
   energies3=zeros(aantal)
   check3=zeros(aantal)
   RIM_check3 = zeros(aantal)
   RIM_E3 = zeros(aantal)

   crew.recprofile = trianglerecovery()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity3[i] = res[2]
      ratios3[i] = res[3]
      energies3[i] = res[4]
      power3[i] = res[5]
      check3[i] = res[9]
      RIM_check3[i] = res[11]
      RIM_E3[i] = res[10]
      

   velocity4 = zeros(aantal)
   power4 = zeros(aantal)
   ratios4=zeros(aantal)
   energies4=zeros(aantal)
   check4=zeros(aantal)
   RIM_check4 = zeros(aantal)
   RIM_E4 = zeros(aantal)

   crew.recprofile = realisticrecovery()

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity4[i] = res[2]
      ratios4[i] = res[3]
      energies4[i] = res[4]
      power4[i] = res[5]
      check4[i] = res[9]
      RIM_check4[i] = res[11]
      RIM_E4[i] = res[10]

   calctime = time.time()-tm

   [min1,sec1] = rowing.vavgto500mtime(velocity1)
   [min2,sec2] = rowing.vavgto500mtime(velocity2)
   [min3,sec3] = rowing.vavgto500mtime(velocity3)
   [min4,sec4] = rowing.vavgto500mtime(velocity4)

   sec1 = sec1+(min1-1)*60.
   sec2 = sec2+(min2-1)*60.
   sec3 = sec3+(min3-1)*60.
   sec4 = sec4+(min4-1)*60.

   # plotjes
   try:
      clf()

      if (doplot==1):
	  plot (power1,velocity1,'-g',label='constant ')
	  plot (power2,velocity2,'-r',label='sinus ')
	  plot (power3,velocity3,'-b',label='triangle ')
	  plot (power4,velocity4,'-k',label='realistic ')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('Velocity (m/s)')


      if (doplot==2):
	  plot (tempos,velocity1,'-g',label='constant')
	  plot (tempos,velocity2,'-r',label='sinus')
	  plot (tempos,velocity3,'-b',label='triangle')
	  plot (tempos,velocity4,'-k',label='realistic')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Velocity (m/s)')

      if (doplot==3):
	  plot (tempos,power1,'-g',label='constant ')
	  plot (tempos,power2,'-r',label='sinus ')
	  plot (tempos,power3,'-b',label='triangle ')
	  plot (tempos,power4,'-k',label='realistic ')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Power (W)')

      if (doplot==4):
	  plot (power1,sec1,'-g',label='constant')
	  plot (power2,sec2,'-r',label='sinus')
	  plot (power3,sec3,'-b',label='triangle')
	  plot (power4,sec4,'-k',label='realistic')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('500m time')

      if (doplot==5):
	  plot (check1,velocity1,'-g',label='constant')
	  plot (check2,velocity2,'-r',label='sinus')
	  plot (check3,velocity3,'-b',label='triangle')
	  plot (check4,velocity4,'-k',label='realistic')
	  legend(loc='best')
	  xlabel("Check (m2/s4)")
	  ylabel('Velocity (m/s)')

      if (doplot == 6):
	  plot (RIM_check1,velocity1,'-g',label='constant')
	  plot (RIM_check2,velocity2,'-r',label='sinus')
	  plot (RIM_check3,velocity3,'-b',label='triangle')
	  plot (RIM_check4,velocity4,'-k',label='realistic')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Check (m/s)')

      if (doplot == 7):
	  plot (RIM_E1,velocity1,'-g',label='constant')
	  plot (RIM_E2,velocity2,'-r',label='sinus')
	  plot (RIM_E3,velocity3,'-b',label='triangle')
	  plot (RIM_E4,velocity4,'-k',label='realistic')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Stroke Efficiency (m)')


      if (doplot == 8):
	  plot (ratios1,velocity1,'-g',label='constant')
	  plot (ratios2,velocity2,'-r',label='sinus')
	  plot (ratios3,velocity3,'-b',label='triangle')
	  plot (ratios4,velocity4,'-k',label='realistic')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('Stroke/Recovery Ratio')


      show()
   except NameError:
      print "No plotting today"

   return calctime

def recoverystyletriangle(tempomin,tempomax,F,crew,rigging,aantal=30,timestep=0.03,doplot=1,timewise=0):

   from crew import flatrecovery,sinusrecovery,trianglerecovery,realisticrecovery
   tm = time.time() 

   tempos = linspace(tempomin,tempomax,aantal)
   velocity1 = zeros(aantal)
   power1 = zeros(aantal)
   ratios1=zeros(aantal)
   energies1=zeros(aantal)
   check1=zeros(aantal)
   RIM_check1 = zeros(aantal)
   RIM_E1 = zeros(aantal)

   crew.recprofile = trianglerecovery(0.1)

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity1[i] = res[2]
      ratios1[i] = res[3]
      energies1[i] = res[4]
      power1[i] = res[5]
      check1[i] = res[9]
      RIM_check1[i] = res[11]
      RIM_E1[i] = res[10]
      
   velocity2 = zeros(aantal)
   power2 = zeros(aantal)
   ratios2=zeros(aantal)
   energies2=zeros(aantal)
   check2=zeros(aantal)
   RIM_check2 = zeros(aantal)
   RIM_E2 = zeros(aantal)

   crew.recprofile = trianglerecovery(0.3)

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity2[i] = res[2]
      ratios2[i] = res[3]
      energies2[i] = res[4]
      power2[i] = res[5]
      check2[i] = res[9]
      RIM_check2[i] = res[11]
      RIM_E2[i] = res[10]

   velocity3 = zeros(aantal)
   power3 = zeros(aantal)
   ratios3=zeros(aantal)
   energies3=zeros(aantal)
   check3=zeros(aantal)
   RIM_check3 = zeros(aantal)
   RIM_E3 = zeros(aantal)

   crew.recprofile = trianglerecovery(0.5)

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity3[i] = res[2]
      ratios3[i] = res[3]
      energies3[i] = res[4]
      power3[i] = res[5]
      check3[i] = res[9]
      RIM_check3[i] = res[11]
      RIM_E3[i] = res[10]
      

   velocity4 = zeros(aantal)
   power4 = zeros(aantal)
   ratios4=zeros(aantal)
   energies4=zeros(aantal)
   check4=zeros(aantal)
   RIM_check4 = zeros(aantal)
   RIM_E4 = zeros(aantal)

   crew.recprofile = trianglerecovery(0.7)

   for i in range(len(tempos)):
      dv = 1
      vend = 4
      crew.tempo = tempos[i]
      catchacceler = 5.0

      while (dv/vend > 0.001):
         res = rowing.energybalance(F,crew,rigging,vend,timestep,0,
				    timewise=timewise,
				    catchacceler=catchacceler)
         dv = res[0]
         vend = res[1]
	 catchacceler = res[14]
      res = rowing.stroke(F,crew,rigging,vend,timestep,10,
			  timewise=timewise,
			  catchacceler=catchacceler)

      velocity4[i] = res[2]
      ratios4[i] = res[3]
      energies4[i] = res[4]
      power4[i] = res[5]
      check4[i] = res[9]
      RIM_check4[i] = res[11]
      RIM_E4[i] = res[10]

   calctime = time.time()-tm

   [min1,sec1] = rowing.vavgto500mtime(velocity1)
   [min2,sec2] = rowing.vavgto500mtime(velocity2)
   [min3,sec3] = rowing.vavgto500mtime(velocity3)
   [min4,sec4] = rowing.vavgto500mtime(velocity4)

   sec1 = sec1+(min1-1)*60.
   sec2 = sec2+(min2-1)*60.
   sec3 = sec3+(min3-1)*60.
   sec4 = sec4+(min4-1)*60.

   # plotjes
   try:
      clf()

      if (doplot==1):
	  plot (power1,velocity1,'-g',label='0.1 ')
	  plot (power2,velocity2,'-r',label='0.3 ')
	  plot (power3,velocity3,'-b',label='0.5 ')
	  plot (power4,velocity4,'-k',label='0.7 ')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('Velocity (m/s)')


      if (doplot==2):
	  plot (tempos,velocity1,'-g',label='0.1')
	  plot (tempos,velocity2,'-r',label='0.3')
	  plot (tempos,velocity3,'-b',label='0.5')
	  plot (tempos,velocity4,'-k',label='0.7')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Velocity (m/s)')

      if (doplot==3):
	  plot (tempos,power1,'-g',label='0.1 ')
	  plot (tempos,power2,'-r',label='sinus ')
	  plot (tempos,power3,'-b',label='triangle ')
	  plot (tempos,power4,'-k',label='realistic ')
	  legend(loc='best')
	  xlabel("tempo (spm)")
	  ylabel('Power (W)')

      if (doplot==4):
	  plot (power1,sec1,'-g',label='0.1')
	  plot (power2,sec2,'-r',label='0.3')
	  plot (power3,sec3,'-b',label='0.5')
	  plot (power4,sec4,'-k',label='0.7')
	  legend(loc='best')
	  xlabel("Power (W)")
	  ylabel('500m time')

      if (doplot==5):
	  plot (check1,velocity1,'-g',label='0.1')
	  plot (check2,velocity2,'-r',label='0.3')
	  plot (check3,velocity3,'-b',label='0.5')
	  plot (check4,velocity4,'-k',label='0.7')
	  legend(loc='best')
	  xlabel("Check (m2/s4)")
	  ylabel('Velocity (m/s)')

      if (doplot == 6):
	  plot (RIM_check1,velocity1,'-g',label='0.1')
	  plot (RIM_check2,velocity2,'-r',label='0.3')
	  plot (RIM_check3,velocity3,'-b',label='0.5')
	  plot (RIM_check4,velocity4,'-k',label='0.7')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Check (m/s)')

      if (doplot == 7):
	  plot (RIM_E1,velocity1,'-g',label='0.1')
	  plot (RIM_E2,velocity2,'-r',label='0.3')
	  plot (RIM_E3,velocity3,'-b',label='0.5')
	  plot (RIM_E4,velocity4,'-k',label='0.7')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('RIM Stroke Efficiency (m)')


      if (doplot == 8):
	  plot (ratios1,velocity1,'-g',label='0.1')
	  plot (ratios2,velocity2,'-r',label='0.3')
	  plot (ratios3,velocity3,'-b',label='0.5')
	  plot (ratios4,velocity4,'-k',label='0.7')
	  legend(loc='best')
	  ylabel("velocity (m/s)")
	  xlabel('Stroke/Recovery Ratio')


      show()
   except NameError:
      print "No plotting today"

   return calctime

def forceseries(Forcemin,Forcemax,tempo,crew,rigging,aantal=10,timestep=.03):

   tm = time.time() 

   crew.tempo=tempo


   Forces = linspace(Forcemin,Forcemax,aantal)
   velocity = zeros(aantal)
   power = zeros(aantal)
   ratios=zeros(aantal)
   energies=zeros(aantal)

   for i in range(len(Forces)):
      dv = 1
      vend = 4
      while (dv/vend > 0.001):
         res = rowing.energybalance(Forces[i],crew,rigging,vend,timestep,0,timewise=timewise)
         dv = res[0]
         vend = res[1]
      res = rowing.stroke(Forces[i],crew,rigging,vend,timestep,10,timewise=timewise)
      velocity[i] = res[2]
      ratios[i] = res[3]
      energies[i] = res[4]
      power[i] = res[5]

   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      subplot(221)
      plot (Forces,velocity)
      xlabel("Force (N)")
      ylabel('Velocity (m/s)')

      subplot(222)
      plot (Forces,power)
      xlabel("Force (N)")
      ylabel('Power (W)')

      subplot(223)
      plot (power,velocity)
      xlabel("Power (W)")
      ylabel('Velocity (m/s)')


      subplot(224)
      plot (Forces,ratios)
      xlabel("Force (N)")
      ylabel('Ratio')

      show()
   except NameError:
      print "No plotting today"

   return calctime

def plot_tempo_v_constantwatt(watt,r,rg,aantal=10,timestep=0.03,Fmin=100,Fmax=760,tempomin=20,tempomax=40):

   tm = time.time() 



   tempoos = linspace(tempomin,tempomax,aantal)

   velocity = zeros(aantal)
   ratios = zeros(aantal)
   watts = zeros(aantal)
   fres = zeros(aantal)
   effs = zeros(aantal)
   
   for i in range(len(tempoos)):
      r.tempo = tempoos[i]
      res = rowing.constantwatt(watt,r,rg,aantal=10,aantal2=15,timestep=timestep,Fmin=Fmin,Fmax=Fmax)
      fres[i] = res[0]
      velocity[i] = res[1]
      ratios[i] = res[2]
      watts[i] = res[3]
      effs[i] = res[4]

      print tempoos[i],velocity[i],watts[i],fres[i],effs[i]

   wattratio = (watts/watts[0])**(1./3.)
   velocity = velocity/wattratio

   res = rowing.vavgto500mtime(velocity)
   mins500 = res[0]
   secs500 = res[1]

   secs500 = secs500+60.*(mins500-1.)

   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      subplot(221)
      plot (tempoos,velocity)
      xlabel("tempo (spm)")
      ylabel('velocity (m/s)')


      subplot(222)
      plot (tempoos,effs)
      xlabel("tempo (spm)")
      ylabel('Efficiency')

      subplot(223)
      plot (tempoos,fres)
      xlabel("tempo (spm)")
      ylabel('Average Stroke Force (N)')

      subplot(224)
      plot (tempoos,ratios)
      xlabel("tempo (spm)")
      ylabel('Drive time fraction')

  
      show()
   except NameError:
      print "No plotting today"

   return calctime

def plot_catchangle_v_constantwatt(watt,r,rg,aantal=10,timestep=0.03):

   tm = time.time() 

   catchanglemin = -1.3
   catchanglemax = -0.7


   catchangles = linspace(catchanglemin,catchanglemax,aantal)

   velocity = zeros(aantal)
   eff = zeros(aantal)
   watts = zeros(aantal)
   

   for i in range(len(catchangles)):
      rg.catchangle=catchangles[i]

      res = rowing.constantwatt(watt,r,rg,timestep=timestep)
      velocity[i] = res[1]
      eff[i] = res[4]
      watts[i] = res[3]
      print degrees(catchangles[i]),rg.dcatch,velocity[i],watts[i]

   wattratio = (watts/watts[0])**(1./3.)
   velocity = velocity/wattratio

   res = rowing.vavgto500mtime(velocity)
   mins500 = res[0]
   secs500 = res[1]

   secs500 = secs500+60.*(mins500-1.)

   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      subplot(221)
      plot (degrees(catchangles),velocity)
      xlabel("catch angle (o)")
      ylabel('Velocity (m/s)')

      subplot(222)
      plot (degrees(catchangles),eff)
      xlabel("catch angle (o)")
      ylabel('Efficiency')

      subplot(223)
      plot (eff,velocity)
      xlabel("Efficiency")
      ylabel('Velocity (m/s)')


      subplot(224)
      plot (degrees(catchangles),secs500)
      xlabel("catch angle (o)")
      ylabel('500m time')

      show()
   except NameError:
      print "No plotting today"

   return calctime

def plot_ratio_v_constantwatt(watt,r,rg,aantal=10,timestep=0.03):

   tm = time.time() 

   lscullmin = 2.6
   lscullmax = 3.3


   lsculls = linspace(lscullmin,lscullmax,aantal)

   velocity = zeros(aantal)
   eff = zeros(aantal)
   watts = zeros(aantal)
   ratios = zeros(aantal)

   velocity2 = zeros(aantal)
   eff2 = zeros(aantal)
   watts2 = zeros(aantal)
   ratios2 = zeros(aantal)

   velocity3 = zeros(aantal)
   eff3 = zeros(aantal)
   watts3 = zeros(aantal)
   ratios3 = zeros(aantal)

   r.tempo = 25.
   watt = 280.

   for i in range(len(lsculls)):
      rg.lscull=lsculls[i]

      res = rowing.constantwatt(watt,r,rg,timestep=timestep)
      velocity[i] = res[1]
      ratios[i] = res[2]
      eff[i] = res[4]
      watts[i] = res[3]
      print r.tempo, lsculls[i],ratios[i],velocity[i],watts[i]

   wattratio = (watts/watts[0])**(1./3.)
   velocity = velocity/wattratio

   relvel = velocity/max(velocity)

   r.tempo = 30.
   watt = 320.

   for i in range(len(lsculls)):
      rg.lscull=lsculls[i]

      res = rowing.constantwatt(watt,r,rg,timestep=timestep)
      velocity2[i] = res[1]
      ratios2[i] = res[2]
      eff2[i] = res[4]
      watts2[i] = res[3]
      print r.tempo, lsculls[i],ratios2[i],velocity2[i],watts2[i]

   wattratio = (watts2/watts2[0])**(1./3.)
   velocity2 = velocity2/wattratio

   relvelb = velocity2/max(velocity2)

   r.tempo = 35.
   watt = 450.

   for i in range(len(lsculls)):
      rg.lscull=lsculls[i]

      res = rowing.constantwatt(watt,r,rg,timestep=timestep)
      velocity3[i] = res[1]
      ratios3[i] = res[2]
      eff3[i] = res[4]
      watts3[i] = res[3]
      print r.tempo, lsculls[i],ratios3[i],velocity3[i],watts3[i]

   wattratio = (watts3/watts3[0])**(1./3.)
   velocity3 = velocity3/wattratio

   relvelb = velocity3/max(velocity3)

   results = vstack((lsculls,velocity,eff,watts,ratios))
   savetxt('v_ratio_T25.txt',results)
   results2 = vstack((lsculls,velocity2,eff2,watts2,ratios2))
   savetxt('v_ratio_T30.txt',results2)
   results3 = vstack((lsculls,velocity3,eff3,watts3,ratios3))
   savetxt('v_ratio_T35.txt',results3)



   calctime = time.time()-tm


   # plotjes
   try:
      clf()

      subplot(221)
      plot (lsculls,velocity,'-g',label='280 W, T=25')
      plot (lsculls,velocity2,'-r',label='320 W, T=30')
      plot (lsculls,velocity3,'-b',label='450 W, T=35')
      legend(loc='best')
      xlabel("L scull (m)")
      ylabel('Velocity (m/s)')

      subplot(222)
      plot (ratios,velocity,'-g',label='280 W, T=25')
      plot (ratios2,velocity2,'-r',label='320 W, T=30')
      plot (ratios3,velocity3,'-b',label='450 W, T=35')
      legend(loc='best')
      xlabel("Ratio")
      ylabel('Velocity (m/s)')

      subplot(223)
      plot (lsculls,relvel,'-g',label='280 W, T=25')
      plot (lsculls,relvela,'-r',label='320 W, T=30')
      plot (lsculls,relvelb,'-b',label='450 W, T=35')
      legend(loc='best')
      xlabel("L scull (m)")
      ylabel('Relative velocity')
 

      subplot(224)
      plot (ratios,relvel,'-g',label='280 W, T=25')
      plot (ratios2,relvela,'-r',label='320 W, T=30')
      plot (ratios3,relvelb,'-b',label='450 W, T=35')
      legend(loc='best')
      xlabel("Ratio")
      ylabel('Relative velocity')

      show()
   except NameError:
      print "No plotting today"

   return calctime

def plot_tempo_power_constantv(velo,r,rg,aantal=10,timestep=0.03,
			       Fmin=50,Fmax=650):

   tm = time.time() 

   tempomin = 24
   tempomax = 33

   tempoos = linspace(tempomin,tempomax,aantal)

   velocity = zeros(aantal)
   ratios = zeros(aantal)
   watts = zeros(aantal)
   peakforce = zeros(aantal)
   eff = zeros(aantal)

   for i in range(len(tempoos)):
      r.tempo = tempoos[i]
      res = rowing.constantvelo(velo,r,rg,timestep=timestep,Fmin=Fmin,Fmax=Fmax)
      velocity[i] = res[1]
      ratios[i] = res[2]
      watts[i] = res[3]
      eff[i]=res[4]
      peakforce[i] = res[0]
      print tempoos[i],velocity[i],watts[i],peakforce[i]

   calctime = time.time()-tm

   watts = watts*(velocity/velocity[0])**3

   # plotjes
   try:
      clf()

      subplot(221)
      plot (tempoos,watts)
      xlabel("tempo (spm)")
      ylabel('Power (W)')


      subplot(222)
      plot (tempoos,eff)
      xlabel("tempo (spm)")
      ylabel('Efficiency')

      subplot(223)
      plot (tempoos,peakforce)
      xlabel("tempo (spm)")
      ylabel('Average Stroke Force (N)')

      subplot(224)
      plot (tempoos,ratios)
      xlabel("tempo (spm)")
      ylabel('Drive time fraction')

  
      show()
   except NameError:
      print "No plotting today"

   return calctime


def plot_inboard_power_constantv(velo,r,rg,aantal=10,timestep=0.03):

   tm = time.time() 

   linmin = 86.0
   linmax = 92.

   lins = linspace(linmin,linmax,aantal)

   velocity = zeros(aantal)
   ratios = zeros(aantal)
   watts = zeros(aantal)
   peakforce = zeros(aantal)
   eff = zeros(aantal)

   for i in range(len(lins)):
      rg.lin = lins[i]/100.
      res = rowing.constantvelo(velo,r,rg,timestep=timestep)
      velocity[i] = res[1]
      ratios[i] = res[2]
      watts[i] = res[3]
      eff[i]=res[4]
      peakforce[i] = (0.5+0.25*pi)*res[0]
      
      print lins[i],velocity[i],watts[i],peakforce[i]


   calctime = time.time()-tm


   # plotjes
   try:
      clf()

#      subplot(221)
      plot (lins,watts)
      xlabel("Inboard (cm)")
      ylabel('Power (W)')


#      subplot(222)
#      plot (lins,eff)
#      xlabel("Inboard (cm)")
#      ylabel('Efficiency')

#      subplot(223)
#      plot (lins,peakforce)
#      xlabel("Inboard (cm)")
#      ylabel('Average Stroke Force (N)')

  
      show()
   except NameError:
      print "No plotting today"

   return calctime

def plot_boatweight_power_constantv(velo,r,rg,aantal=10,timestep=0.01):

   tm = time.time() 

   mborg = rg.mb

   mbmin = 14.0
   mbmax = 40.0

   mbs = linspace(mbmin,mbmax,aantal)

   velocity = zeros(aantal)
   ratios = zeros(aantal)
   watts = zeros(aantal)
   peakforce = zeros(aantal)
   eff = zeros(aantal)


   for i in range(len(mbs)):
      rg.mb = mbs[i]
      res = rowing.constantvelo(velo,r,rg,timestep=timestep,aantal2=10,Fmin=100,Fmax=700)
      velocity[i] = res[1]
      ratios[i] = res[2]
      watts[i] = res[3]
      eff[i]=res[4]
      peakforce[i] = (0.5+0.25*pi)*res[0]
      
      print mbs[i],velocity[i],watts[i],peakforce[i]


   calctime = time.time()-tm

   rg.mb = mborg

   # plotjes
   try:
      clf()

      subplot(221)
      plot (mbs,watts)
      xlabel("Boat Weight (kg)")
      ylabel('Power (W)')


      subplot(222)
      plot (mbs,eff)
      xlabel("Boat Weight (kg)")
      ylabel('Efficiency')

      subplot(223)
      plot (mbs,peakforce)
      xlabel("Boat Weight (kg)")
      ylabel('Average Stroke Force (N)')

  
      show()
   except NameError:
      print "No plotting today"

   return calctime

def atkinson(timestep=0.01,factor=0.45,doplot=1,h1=0.75,h2=1.0,
             timewise=0,x1=0.02,x2=0.39,bladearea=0.071,
             lscull=3.05,lin=0.86,strokelength=1.31,constantdrag=0):
   from crew import trapezium
   from crew import trianglerecovery,sinusrecovery,flatrecovery

   r = crew(mc=90.0,tempo=29.4,strokelength=strokelength)
   r.strokeprofile = trapezium(x1=x1,x2=x2,h1=h1,h2=h2)


   ratio = r.strokeprofile.ratio
   rg = rigging(mb=14.,catchangle=-1.18,lin=lin,
                bladearea=bladearea,lscull=lscull)


   factor2 = (rg.lscull-rg.lin)/rg.lin
#   print factor2

   F = ratio*368.*factor*factor2

   aantal=100

   x = linspace(0,r.strokelength,aantal)
   y1 = zeros(aantal)

   for i in range(len(x)):
      y1[i] = r.forceprofile(F,x[i])


   # op snelheid komen
   dv = 1.0
   vend = 4.0

   tm = time.time()

   while (dv/vend > 0.001):
      res = rowing.atkinsoncalc(F,r,rg,vend,timestep,0,timewise=timewise,constantdrag=constantdrag)
      dv = res[0]
      vend = res[1]

   res = rowing.stroke_atkinson(F,r,rg,vend,timestep,10,timewise=timewise,constantdrag=constantdrag)
   velocity = res[2]
   ratios = res[3]
   energies = res[4]
   power = res[5]


   res2 = rowing.atkinsoncalc(F,r,rg,vend,timestep,doplot=doplot,doprint=1,
                               timewise=timewise,constantdrag=constantdrag)

   velocity2 = res2[2]
   ratios2 = res2[3]
   energies2 = res2[4]
   power2 = res2[5]

   displacement = rg.mb+rg.Nrowers*r.mc
   res = rowing.drag_eq(displacement,velocity,alfaref=3.2,doprint=1,constantdrag=constantdrag)

   print "Velocity :",velocity,"  m/s"
   print "Ratio    :",ratios
   print "Power    :",power," W"
   print "Energy   :",energies," J"
   print "dv       :",res2[0]
   print "vend     :",res2[1]
   print "vmin     :",res2[7]
   print "vmax     :",res2[8]

   calctime = time.time()-tm
   

   return calctime

def james_hm2min(timestep=0.01,factor=0.86,doplot=1,h1=1.0,h2=0.8,
             timewise=0,x1=0.03,x2=0.35,bladearea=1.212e-1):
   from crew import trapezium
   from crew import trianglerecovery,sinusrecovery,flatrecovery

   r = crew(mc=88.5,tempo=36.0,strokelength=1.37)
   r.strokeprofile = trapezium(x1=x1,x2=x2,h1=h1,h2=h2)

   ratio = r.strokeprofile.ratio
   rg = rigging(Nrowers=2,mb=27.,roworscull='row',catchangle=-1.18,lin=1.16,
                bladearea=bladearea,bladelength=0.55,spread=0.86,lscull=3.76)


   factor2 = rg.lscull/(rg.lscull-rg.lin)

   F = ratio*368.*factor*factor2

   aantal=100

   x = linspace(0,r.strokelength,aantal)
   y1 = zeros(aantal)

   for i in range(len(x)):
      y1[i] = r.forceprofile(F,x[i])


   # op snelheid komen
   dv = 1.0
   vend = 4.0

   tm = time.time()

   while (dv/vend > 0.001):
      res = rowing.atkinsoncalc(F,r,rg,vend,timestep,0,timewise=timewise)
      dv = res[0]
      vend = res[1]

   res = rowing.stroke_atkinson(F,r,rg,vend,timestep,10,timewise=timewise)
   velocity = res[2]
   ratios = res[3]
   energies = res[4]
   power = res[5]


   res2 = rowing.atkinsoncalc(F,r,rg,vend,timestep,doplot=doplot,doprint=1,
                               timewise=timewise)

   velocity2 = res2[2]
   ratios2 = res2[3]
   energies2 = res2[4]
   power2 = res2[5]



   print "Velocity :",velocity,"  m/s"
   print "Ratio    :",ratios
   print "Power    :",power," W"
   print "Energy   :",energies," J"
   print "dv       :",res[0]

   calctime = time.time()-tm
   

   return calctime

def powerseries(powers,r,rg):
   
   for pw in powers:
      res = rowing.constantwatt(pw,r,rg)
      [mins,secs] = rowing.vavgto500mtime(res[1])
      print pw,'W  ',mins,':',secs

def ergtoboat(splits,r,rg,tempos,erg):

   ratio = 0.4
   
   for tempo in tempos:
      r.tempo = tempo

      print "----------------------------------------"
      print "Tempo       ",tempo, " /min"
      print ""
      print "erg split     erg P    total P      boat split"
      
      for split in splits:
         mins = split[0]
         secs = split[1]
      
         res = rowing.ergtopower(mins,secs,ratio,r,erg)
         totalpower = res[0]
         ergpower = res[1]

         res = rowing.constantwatt(totalpower,r,rg)
         [bmins,bsecs] = rowing.vavgto500mtime(res[1])
         bmins = int(bmins)
         bsecs = int(10*bsecs)/10.
         
         print mins,":",secs,"  ",int(ergpower),"   ",int(totalpower),"  ",bmins,":",bsecs

def tempopower(r,rg,tp,pw):

    res = rowing.constantwatt(pw,r,rg,timestep = 0.01,aantal = 15,aantal2=15)
    print pw,res[3]
    print 'Split ',rowing.vavgto500mtime(res[1])

def tempopowererg(r,rg,erg,tp,pwd,theconst=0.0):
    
    res = rowing.constantwatt_ergdisplay(pwd,r,erg,timestep=0.01,aantal=10,aantal2=10,theconst=theconst)
    print res
    pw = res[3]
    res = rowing.constantwatt(pw,r,rg,timestep = 0.01,aantal = 15,aantal2=15)
    print pw,res[3]
    print 'Split ',rowing.vavgto500mtime(res[1])
