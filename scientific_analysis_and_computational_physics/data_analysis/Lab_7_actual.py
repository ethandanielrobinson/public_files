# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 10:42:11 2023

@author: ethan
"""

#%% LAB 7
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P7.1.a
#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# First, we define our constants
D=2
L=3
N=80
lam=((np.pi/L)**2)*D

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

# this is the actual center-cell grid with 2 ghost points
x=np.linspace(0-(h/2),L+(h/2),N+1) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# We now generate our initial conditions.
T = np.sin(np.pi*(x/L)) #copied from the text
start=np.copy(T) #This is for the exact soultion

Tnew = np.zeros_like(T) #we initialize Tnew
j = 0
t = 0
tmax = 2
plt.figure(1) # Open the figure window

#and define our weight co-efficient
weight=(D*tau)/(h**2) #this is from equation 7.10


# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    Tnew[1:-1]=T[1:-1]+weight*(T[2:]-(2*T[1:-1])+T[0:-2])
    Tnew[0]=-Tnew[1] # setting the boundary condition at x=0 to be 0
    Tnew[-1]=-Tnew[-2] # setting the boundary condition at x=L to be 0
    
    #and find the exact solution with f(t)
    f=np.exp(-lam*t)
    exact=start*f
    
    #And find the error
    error = np.sqrt( np.mean( (T - exact)**2 ))
    
    #we now update yold and y
    T=np.copy(Tnew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,T,'bo',x,exact,'r-')
        plt.xlabel('x')
        plt.ylabel('T')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,0.6])
        plt.xlim([0,3])
        plt.draw() # Draw the plot
        print(error)
        plt.pause(0.1) # Give the computer time to draw

#%% P7.1.b
#-------------------------------------------------
# Same as part a, except D is now variable as well
#-------------------------------------------------

#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# First, we define our constants
L=3
N=20

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

# this is the actual center-cell grid with 2 ghost points
x=np.linspace(0-(h/2),L+(h/2),N+1) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# -------------------- THIS PART IS DIFFERENT
din=input("What value would you like for D? ")
D=float(din)
lam=((np.pi/L)**2)*D
#--------------------------------------------

# We now generate our initial conditions.
T = np.sin(np.pi*(x/L)) #copied from the text
start=np.copy(T) #This is for the exact soultion

Tnew = np.zeros_like(T) #we initialize Tnew
j = 0
t = 0
tmax = 2
plt.figure(1) # Open the figure window

#and define our weight co-efficient
weight=(D*tau)/(h**2) #this is from equation 7.10

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    Tnew[1:-1]=T[1:-1]+weight*(T[2:]-(2*T[1:-1])+T[0:-2])
    Tnew[0]=-Tnew[1] # setting the boundary condition at x=0 to be 0
    Tnew[-1]=-Tnew[-2] # setting the boundary condition at x=L to be 0
    
    #and find the exact solution with f(t)
    f=np.exp(-lam*t)
    exact=start*f
   
    #And find the error
    error = np.sqrt( np.mean( (T - exact)**2 ))
   
    #we now update yold and y
    T=np.copy(Tnew)
   
    if j % 50 == 0:
       plt.clf() # clear the figure window
       plt.plot(x,T,'bo',x,exact,'r-')
       plt.xlabel('x')
       plt.ylabel('T')
       plt.title('time={:1.3f}'.format(t))
       plt.ylim([0,0.6])
       plt.xlim([0,3])
       plt.draw() # Draw the plot
       print(error)
       plt.pause(0.1) # Give the computer time to draw
       
#%% P7.1.c

# Same as part a, but now we have different boundary conditions

#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# First, we define our constants
D=2
L=3
N=20
lam=((np.pi/L)**2)*D

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

# this is the actual center-cell grid with 2 ghost points
x=np.linspace(0-(h/2),L+(h/2),N+1) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# We now generate our initial conditions.
T = np.sin(np.pi*(x/L)) #copied from the text
start=np.copy(T) #This is for the exact soultion

Tnew = np.zeros_like(T) #we initialize Tnew
j = 0
t = 0
tmax = 2
plt.figure(2) # Open the figure window

#and define our weight co-efficient
weight=(D*tau)/(h**2) #this is from equation 7.10


# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    Tnew[1:-1]=T[1:-1]+weight*(T[2:]-(2*T[1:-1])+T[0:-2])
    # THIS PART IS DIFFERENT-----------------------------------------
    Tnew[0]=Tnew[1] # setting the boundary condition at x=0 to be T'=0
    Tnew[-1]=Tnew[-2] # setting the boundary condition at x=L to be T'=0
    
    #and find the exact solution with f(t)
    f=np.exp(-lam*t)
    exact=start*f
    
    #And find the error
    error = np.sqrt( np.mean( (T - exact)**2 ))
    
    #we now update yold and y
    T=np.copy(Tnew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,T,'bo',x,exact,'r-')
        plt.xlabel('x')
        plt.ylabel('T')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,1])
        plt.xlim([0,3])
        plt.draw() # Draw the plot
        print(error)
        plt.pause(0.1) # Give the computer time to draw
        
#%% P7.2.a

#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# we want to be able to compare tau values.
tau1 = 0.5
tin=input("What value would you like for tau? ")
tau2=float(tin)
tmax = 20.
t1 = np.arange(0,tmax,tau1)
t2 = np.arange(0,tmax,tau2)
y1 = np.zeros_like(t1)
y2 = np.zeros_like(t2)

# and set the inital condition
y1[0]=1
y2[0]=1


amount1=len(t1) #how many times do we want this to rum
amount2=len(t2)

j=0
# calculate the good one
while j<amount1-1:
    y1[j+1]=y1[j]*(1-tau1)
    j=j+1

#and the bad one
s=0
while s<amount2-1:
    y2[s+1]=y2[s]*(1-tau2)
    s=s+1
    
plt.figure(3) # Open the figure window    
plt.plot(t1,y1,'b',t2,y2,"r") #y1 will be blue, y2 will be red
plt.title('P7.4.a')
plt.legend(["tau=0.5","tau=input"])
plt.xlabel('t')

#%% P7.2.b

# Semi-implicit method

#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# we want to be able to compare tau values.
tau1 = 0.5
tin=input("What value would you like for tau? ")
tau2=float(tin)
tmax = 20.
t1 = np.arange(0,tmax,tau1)
t2 = np.arange(0,tmax,tau2)
y1 = np.zeros_like(t1)
y2 = np.zeros_like(t2)

# and set the inital condition
y1[0]=1
y2[0]=1


amount1=len(t1) #how many times do we want this to rum
amount2=len(t2)
weight1=(tau1-2)/(tau1+2)
weight2=(tau2-2)/(tau2+2)

j=0
# calculate the good one
while j<amount1-1:
    y1[j+1]=-y1[j]*weight1
    j=j+1

#and the bad one
s=0
while s<amount2-1:
    y2[s+1]=-y2[s]*weight2
    s=s+1
    
plt.figure(4) # Open the figure window    
plt.plot(t1,y1,'b',t2,y2,"r") #y1 will be blue, y2 will be red
plt.title('P7.4.b')
plt.legend(["tau=0.5","tau=input"])
plt.xlabel('t')

#%% P7.2.c

#Fully Implicit method

#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# we want to be able to compare tau values.
tau1 = 0.5
tin=input("What value would you like for tau? ")
tau2=float(tin)
tmax = 20.
t1 = np.arange(0,tmax,tau1)
t2 = np.arange(0,tmax,tau2)
y1 = np.zeros_like(t1)
y2 = np.zeros_like(t2)

# and set the inital condition
y1[0]=1
y2[0]=1


amount1=len(t1) #how many times do we want this to rum
amount2=len(t2)
weight1=1/(1+tau1) # THIS PART IS DIFFERENT
weight2=1/(1+tau2) #-----------------------

j=0
# calculate the good one
while j<amount1-1:
    y1[j+1]=y1[j]*weight1 #THIS PART IS DIFFERENT
    j=j+1

#and the bad one
s=0
while s<amount2-1:
    y2[s+1]=y2[s]*weight2 # THIS PART IS DIFFERENT
    s=s+1
    
plt.figure(6) # Open the figure window    
plt.plot(t1,y1,'b',t2,y2,"r") #y1 will be blue, y2 will be red
plt.title('P7.4.c')
plt.legend(["tau=0.5","tau=input"])
plt.xlabel('t')

#%% P7.3.a
# We want to solve the problem from part one using matricies and the implicit method.
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
D=2
L=3
N=40
lam=((np.pi/L)**2)*D

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

# this is the actual center-cell grid with 2 ghost points
x=np.linspace(0-(h/2),L+(h/2),N+1) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# We first define our A matrix--------------------------------------------
A=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N,1):
    A[j,j-1]=-1
    A[j,j]=value+2
    A[j,j+1]=-1

#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5

# And define B as well --------------------------
B=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N,1):
    B[j,j-1]=1
    B[j,j]=value-2
    B[j,j+1]=1

# We now generate our initial conditions.
T = np.sin(np.pi*(x/L)) #copied from the text
start=np.copy(T) #This is for the exact soultion

j = 0
t = 0
tmax = 5
plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@T
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    T = la.solve(A,r)
    
    #and find the exact solution with f(t)
    f=np.exp(-lam*t)
    exact=start*f
    
    #And find the error
    error = np.sqrt( np.mean( (T - exact)**2 ))
    
    
    if j % 2 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,T,'bo',x,exact,'r-')
        plt.xlabel('x')
        plt.ylabel('T')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,0.6])
        plt.xlim([0,3])
        plt.draw() # Draw the plot
        print(error)
        plt.pause(0.1) # Give the computer time to draw
        
#%% P7.3.b
# We want to solve the problem from part one using matricies and the implicit method.
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# First, we define our constants
din=input("What value would you like for D? ")
D=float(din)
L=3
N=40
lam=((np.pi/L)**2)*D

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

# this is the actual center-cell grid with 2 ghost points
x=np.linspace(0-(h/2),L+(h/2),N+1) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# We first define our A matrix--------------------------------------------
A=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N,1):
    A[j,j-1]=-1
    A[j,j]=value+2
    A[j,j+1]=-1

#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5

# And define B as well --------------------------
B=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N,1):
    B[j,j-1]=1
    B[j,j]=value-2
    B[j,j+1]=1

# We now generate our initial conditions.
T = np.sin(np.pi*(x/L)) #copied from the text
start=np.copy(T) #This is for the exact soultion

j = 0
t = 0
tmax = 5
plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@T
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    T = la.solve(A,r)
    
    #and find the exact solution with f(t)
    f=np.exp(-lam*t)
    exact=start*f
    
    #And find the error
    error = np.sqrt( np.mean( (T - exact)**2 ))
    
    
    if j % 2 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,T,'bo',x,exact,'r-')
        plt.xlabel('x')
        plt.ylabel('T')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,0.6])
        plt.xlim([0,3])
        plt.draw() # Draw the plot
        print(error)
        plt.pause(0.1) # Give the computer time to draw

#%% P7.3.c
# We want to solve the problem from part one using matricies and the implicit method.
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
D=2
L=3
N=40
lam=((np.pi/L)**2)*D

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

# this is the actual center-cell grid with 2 ghost points
x=np.linspace(0-(h/2),L+(h/2),N+1) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# We first define our A matrix--------------------------------------------
A=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N,1):
    A[j,j-1]=-1
    A[j,j]=value+2
    A[j,j+1]=-1

#And set the boundry conditions (in this case, x=0 at boundaries)
# THIS PART IS DIFFERENT #
A[0,0] = 1/h
A[0,1] = -1/h
A[-1,-1] = 1/h
A[-1,-2] = -1/h

# And define B as well --------------------------
B=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N,1):
    B[j,j-1]=1
    B[j,j]=value-2
    B[j,j+1]=1

# We now generate our initial conditions.
T = np.sin(np.pi*(x/L)) #copied from the text
start=np.copy(T) #This is for the exact soultion

j = 0
t = 0
tmax = 5
plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@T
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    T = la.solve(A,r)
    
    #and find the exact solution with f(t)
    f=np.exp(-lam*t)
    exact=start*f
    
    #And find the error
    error = np.sqrt( np.mean( (T - exact)**2 ))
    
    
    if j % 1 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,T,'bo',x,exact,'r-')
        plt.xlabel('x')
        plt.ylabel('T')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,1])
        plt.xlim([0,3])
        plt.draw() # Draw the plot
        print(error)
        plt.pause(0.1) # Give the computer time to draw
#%% TEST SPACE
# Let's now generate our matricies A and B
#Boilerplate
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
D=2
L=3
N=40
tau=0.001
# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N,retstep=True) 

B=np.zeros((N+1,N+1))
value=(2*(h**2))/(tau*D) #the variable part of our matrix

for j in range(1,N-1,1):
    B[j,j-1]=-1
    B[j,j]=value-2
    B[j,j+1]=-1