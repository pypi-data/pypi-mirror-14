from math import *

class standaardfunctie:
   def __init__(self,favg=200):
      self.favg = 200

   def forceprofile(self,favg,x):
      return favg*x

class anderefunctie:
   def __init__(self,favg=200):
      self.favg = 200

   def forceprofile(self,favg,x):
      if x>0.5:
         f=favg*(1-x)
      else:
         f = 100.

      return f

class testfun:
   def __init__(self,fun=standaardfunctie(100)):
      self.fun = fun
      
   def forceprofile(self,favg,x):
      return self.fun.forceprofile(favg,x)

