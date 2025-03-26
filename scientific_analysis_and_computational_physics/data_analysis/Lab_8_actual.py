# -*- coding: utf-8 -*-
"""

@author: ethan
"""

#%% LAB 8
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P8.1 SEE ADDENDUM #1.
#%% P8.2.a
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from P7.3 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
m=1 # using atomic units
hbar=1 # using atomic units
L=10 # As specified on my thing
N=200 # As specified by P8.2.a
sig=2 # as specified in P8.2.a
p=-2*np.pi # as specified in P.2.a

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(-L,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(-L-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# And then define the following composite 
Areal=4*(h**2)*m
Aimg=(0.0+1.0j)*Areal
Amain=-(Aimg)/(tau*hbar)+2 #Since V(x) is zero inside the box
# We don't need to worry about  the V(x) bit
Bmain=-((Aimg)/(tau*hbar)+2)

# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    A[j,j-1]=-1
    A[j,j]=Amain
    A[j,j+1]=-1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    B[j,j-1]=1
    B[j,j]=Bmain
    B[j,j+1]=1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5
    
# We now generate our initial conditions.
var1=(0.0+1.0j)*p
Psi=np.exp(((-(1/2)*(x**2))/(sig**2))+((var1*x)/1))/(np.sqrt(sig*np.sqrt(sig)))
start=np.copy(Psi) #This is for the exact soultion

j = 0
t = 0
tmax = 20
plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@Psi
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    Psi = la.solve(A,r)
    Psireal=np.real(Psi)
    Pconj=np.conj(Psi)
    Pabs=Pconj*Psi
       
    
    if j % 10 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,Psireal,'b',x,Pabs,'r')
        plt.xlabel('x')
        plt.ylabel('Psi (real)')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-1,1])
        plt.xlim([-10,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
#%% P8.2.b
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from P7.3 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
m=1 # using atomic units
hbar=1 # using atomic units
L=10 # As specified on my thing
N=200 # As specified by P8.2.a
sig=2 # as specified in P8.2.a
p=-2*np.pi # as specified in P.2.a

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(-L,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(-L-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# And then define the following composite 
Areal=4*(h**2)*m
Aimg=(0.0+1.0j)*Areal
Amain=-(Aimg)/(tau*hbar)+2 #Since V(x) is zero inside the box
# We don't need to worry about  the V(x) bit
Bmain=-((Aimg)/(tau*hbar)+2)

# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    A[j,j-1]=-1
    A[j,j]=Amain
    A[j,j+1]=-1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    B[j,j-1]=1
    B[j,j]=Bmain
    B[j,j+1]=1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5
    
# We now generate our initial conditions.
var1=(0.0+1.0j)*p
Psi=np.exp(((-(1/2)*(x**2))/(sig**2))+((var1*x)/1))/(np.sqrt(sig*np.sqrt(sig)))
start=np.copy(Psi) #This is for the exact soultion

j = 0
t = 0
tmax = 20
plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@Psi
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    Psi = la.solve(A,r)
    Psireal=np.real(Psi)
    Pconj=np.conj(Psi)
    Pabs=Pconj*Psi
    
    
    # We need to find the integral of Pabs
    vols=np.real(Pabs*h) #the reals func just takes the 0j term off
    norm=np.sum(vols) #the edge points are baisicly zero
    # running a little bit high (apx 1.25), but I don't know how to fix this   
    
    if j % 10 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,Psireal,'b',x,Pabs,'r')
        plt.xlabel('x') 
        plt.ylabel('Psi (real)')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-1,1])
        plt.xlim([-10,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        print(norm)
        
#%% P8.2.c
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from P7.3 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
m=1 # using atomic units
hbar=1 # using atomic units
L=10 # As specified on my thing
sig=2
N=200 # As specified by P8.2.a

p=-2*np.pi # as specified in P.2.a

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(-L,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(-L-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

# And then define the following composite 
Areal=4*(h**2)*m
Aimg=(0.0+1.0j)*Areal
Amain=-(Aimg)/(tau*hbar)+2 #Since V(x) is zero inside the box
# We don't need to worry about  the V(x) bit
Bmain=-((Aimg)/(tau*hbar)+2)

# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    A[j,j-1]=-1
    A[j,j]=Amain
    A[j,j+1]=-1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    B[j,j-1]=1
    B[j,j]=Bmain
    B[j,j+1]=1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5
    
# We now generate our initial conditions.
var1=(0.0+1.0j)*p
Psi=np.exp(((-(1/2)*(x**2))/(sig**2))+((var1*x)/1))/(np.sqrt(sig*np.sqrt(sig)))
start=np.copy(Psi) #This is for the exact soultion

j = 0
t = 0
tmax = 200 # WE WANT OUR SIM TO RUN FOR A NICE LONG WHILE
plt.figure(5) # Open the figure window

# We need to intialize our expectation value array so we can plot it
count=int(tmax/tau)+2 #this plus 2 is to make up for a fault in the calculation program
exphold=np.zeros(count,dtype=np.complex_)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@Psi
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    Psi = la.solve(A,r)
    Psireal=np.real(Psi)
    Pconj=np.conj(Psi)
    Pabs=Pconj*Psi
    
    # ADDED PART ------------------------------------------------------------------------------------
    exptemp=Pconj*x*Psi
    expX=np.sum(exptemp*h)
    exphold[j]=expX
    
    
    # We need to find the integral of Pabs
    vols=np.real(Pabs*h) #the reals bit just takes the 0j term off
    norm=np.sum(vols) #the edge points are baisicly zero
    # running a little bit high (apx 1.25), but I don't know how to fix this   
    
    if j % 500 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,Psireal,'b',x,Pabs,'r')
        plt.xlabel('x') 
        plt.ylabel('Psi (real)')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-1,1])
        plt.xlim([-10,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
# create the t values
tlist=np.linspace(0,tmax,count)
expplot=np.real(exphold)

plt.figure(3)
plt.plot(tlist,expplot,'g') #will be green
plt.title('P8.2.c')
plt.legend(['<x>'])
plt.xlabel('t')

#eventualy reaches resonance

#%% P8.2.d
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from P7.3 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
m=1 # using atomic units
hbar=1 # using atomic units
L=10 # As specified on my thing
N=200 # As specified by P8.2.a
p=-2*np.pi # as specified in P.2.a

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(-L,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(-L-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

sin=input("What value would you like for sigma? ")
sig=float(sin)

# And then define the following composite 
Areal=4*(h**2)*m
Aimg=(0.0+1.0j)*Areal
Amain=-(Aimg)/(tau*hbar)+2 #Since V(x) is zero inside the box
# We don't need to worry about  the V(x) bit
Bmain=-((Aimg)/(tau*hbar)+2)

# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    A[j,j-1]=-1
    A[j,j]=Amain
    A[j,j+1]=-1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    B[j,j-1]=1
    B[j,j]=Bmain
    B[j,j+1]=1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5
    
# We now generate our initial conditions.
var1=(0.0+1.0j)*p
Psi=np.exp(((-(1/2)*(x**2))/(sig**2))+((var1*x)/1))/(np.sqrt(sig*np.sqrt(sig)))
start=np.copy(Psi) #This is for the exact soultion

j = 0
t = 0
tmax = 200 # WE WANT OUR SIM TO RUN FOR A NICE LONG WHILE
plt.figure(5) # Open the figure window

# We need to intialize our expectation value array so we can plot it
count=int(tmax/tau)+2 #this plus 2 is to make up for a fault in the calculation program
exphold=np.zeros(count,dtype=np.complex_)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@Psi
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    Psi = la.solve(A,r)
    Psireal=np.real(Psi)
    Pconj=np.conj(Psi)
    Pabs=Pconj*Psi
    
    # ADDED PART ------------------------------------------------------------------------------------
    exptemp=Pconj*x*Psi
    expX=np.sum(exptemp*h)
    exphold[j]=expX
    
    
    # We need to find the integral of Pabs
    vols=np.real(Pabs*h) #the reals bit just takes the 0j term off
    norm=np.sum(vols) #the edge points are baisicly zero
    # running a little bit high (apx 1.25), but I don't know how to fix this   
    
    if j % 20 == 0: #designed to run a bit slower this time
        plt.clf() # clear the figure window
        plt.plot(x,Psireal,'b',x,Pabs,'r')
        plt.xlabel('x') 
        plt.ylabel('Psi (real)')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-1,1])
        plt.xlim([-10,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
# create the t values
tlist=np.linspace(0,tmax,count)
expplot=np.real(exphold)

plt.figure(4)
plt.plot(tlist,expplot,'g') #will be green
plt.title('P8.2.d')
plt.legend(['<x>'])
plt.xlabel('t')

# Takes a lot longer to reach the resonant frequency

#%% P8.3.a & P8.3.b
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from P7.3 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
m=1 # using atomic units
hbar=1 # using atomic units
L=10 # As specified on my thing
N=500 # with the larger area, we want a bit more points
sig=2 # as specified in P8.2.a
p=2*np.pi # as specified in P.2.a

# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(-2*L,3*L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(-2*L-(h/2),3*L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

Vin=input("<E>. is 19.8642. What value would you like for V0? ")
V0=float(Vin)


# We now initialize the V function
V=np.zeros_like(x)
turn1=int((2.98*L+h/2)//h)+1
turn2=int((3*L+h/2)//h)+1 #Finding the edges of the barrier
V[turn1:turn2]=V0


# And then define the following composite 
Areal=4*(h**2)*m
Aimg=(0.0+1.0j)*Areal
V1=((2*(h**2)*m)/(hbar**2))
Amain=-(Aimg)/(tau*hbar)+2+V1*V
# We don't need to worry about  the V(x) bit
Bmain=-((Aimg)/(tau*hbar)+2)+V1*V

# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    A[j,j-1]=-1
    A[j,j]=Amain[j]
    A[j,j+1]=-1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    B[j,j-1]=1
    B[j,j]=Bmain[j]
    B[j,j+1]=1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5
A[0,1] = 0.5
A[-1,-1] = 0.5
A[-1,-2] = 0.5
    
# We now generate our initial conditions.
var1=(0.0+1.0j)*p
Psi=np.exp(((-(1/2)*(x**2))/(sig**2))+((var1*x)/1))/(np.sqrt(sig*np.sqrt(sig)))
start=np.copy(Psi) #This is for the exact soultion

j = 0
t = 0
tmax = 40 #lets run it for 30 seconds
plt.figure(5) # Open the figure window

#create the reference funciton
refV=V/V0


# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@Psi
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 0
    r[-1] = 0
    
    # Solve AT = r. The T we get is for the next time step.
    # We don't need to keep track of previous T values, so just
    # load the new T directly into T itself
    Psi = la.solve(A,r)
    Psireal=np.real(Psi)
    Pconj=np.conj(Psi)
    Pabs=Pconj*Psi
       
    
    if j % 5 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,Psireal,'b',x,Pabs,'r',x,refV,'g')
        plt.xlabel('x')
        plt.ylabel('Psi (real)')
        plt.title('time={:1.3f}'.format(t))
        plt.legend(['Psi',"Psi*Psi","V"])
        plt.ylim([-1,1])
        plt.xlim([-20,30])
        plt.draw() # Draw the plot
        plt.pause(0.05) # Give the computer time to draw

#%% Test Space
V=np.zeros_like(x)
turn1=int((2.98*L+h/2)//h)+1
turn2=int((3*L+h/2)//h)+1 #Finding the edges of the barrier
V[turn1:turn2]=V0
