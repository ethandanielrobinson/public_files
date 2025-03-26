# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 19:55:30 2023

@author: ethan
"""

#%% LAB 10
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P10.1.i
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points

#we want to be able to define our own tau
tin=input("What value would you like for tau? ")
tau=float(tin)

#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N-1,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid

x=np.linspace(0-(h/2),L+(h/2),N) #this is the actual center-cell grid with 2 ghost points
#--0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0

# We now generate our initial conditions.
expo1=-200*(((x/L)-(1/2)))**2
r = 1+np.exp(expo1) #copied from the text
# and the initial velocity
v=np.ones_like(x)

# WE DONT NEED A BACK STEP!

rnew = np.zeros_like(r)
j = 0
t = 0
tmax = 20
plt.figure(1) # Open the figure window

# one last thing: we define our weight (tau/2h)
weight=tau/(2*h)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    rnew[1:-1]=r[1:-1]+weight*(r[0:-2]*v[0:-2]-r[2:]*v[2:])
    rnew[0]=-rnew[1]+2 # setting the boundary condition at x=0 to be 1
    rnew[-1]=-rnew[-2]+2 # setting the boundary condition at x=L to be 1
    
    #we now update yold and y
    rold=np.copy(r)
    r=np.copy(rnew)
    
    if j % 20 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,r,'b-')
        plt.xlabel('x')
        plt.ylabel('r')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,2])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
# THIS DOESNT WORK

#%% P10.1.ii
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points

#we want to be able to define our own tau
tin=input("What value would you like for tau? ")
tau=float(tin)

#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N-1,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid

x=np.linspace(0-(h/2),L+(h/2),N) #this is the actual center-cell grid with 2 ghost points
#--0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0

# We now generate our initial conditions.
expo1=-200*(((x/L)-(1/2)))**2
r = 1+np.exp(expo1) #copied from the text
# and the initial velocity
v0=1
v=np.ones_like(x)*v0 # We Assume v0 to be constant

#------------------
#QUESTION?  WHY DOESNT V CHANGE OVER TIME

# WE DONT NEED A BACK STEP!

rnew = np.zeros_like(r)
j = 0
t = 0
tmax = 20
plt.figure(1) # Open the figure window

# one last thing: we define our weights
weight=tau/(2*h)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    rnew[1:-1]=r[1:-1]+weight*(r[0:-2]*v[0:-2]-r[2:]*v[2:])
    rnew[0]=2-rnew[1] # setting the boundary condition at x=0 to be 1
    rnew[-1]=rnew[-2]+rnew[3]-rnew[-4] # boundary conditions from the book
    
    #we now update yold and y
    rold=np.copy(r)
    r=np.copy(rnew)
    
    if j % 20 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,r,'b-')
        plt.xlabel('x')
        plt.ylabel('r')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,2])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
# THIS DOESNT WORK EITHER :(

#%% P10.2
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points

#we want to be able to define our own tau
tin=input("What value would you like for tau? Stablility occurs around 0.0251: ")
tau=float(tin)

#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N-1,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid

x=np.linspace(0-(h/2),L+(h/2),N) #this is the actual center-cell grid with 2 ghost points
#--0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0

# We now generate our initial conditions.
expo1=-200*(((x/L)-(1/2)))**2
r = 1+np.exp(expo1) #copied from the text
# and the initial velocity
v0=1
v=np.ones_like(x)*v0 # We Assume v0 to be constant

#------------------
#QUESTION?  WHY DOESNT V CHANGE OVER TIME

# WE DONT NEED A BACK STEP!

rnew = np.zeros_like(r)
j = 0
t = 0
tmax = 9
plt.figure(1) # Open the figure window

# one last thing: we define our weights
weight1=(v0*tau)/(2*h)
weight2=((v0**2)*(tau**2))/(2*(h**2))

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    rnew[1:-1]=r[1:-1]-weight1*(r[2:]-r[0:-2])+weight2*(r[2:]-2*r[1:-1]+r[0:-2])
    rnew[0]=2-rnew[1] # setting the boundary condition at x=0 to be 1
    rnew[-1]=-rnew[-2]+2 # setting the boundary condition at x=L to be 1
    
    #we now update yold and y
    rold=np.copy(r)
    r=np.copy(rnew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,r,'b-')
        plt.xlabel('x')
        plt.ylabel('r')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,2.25])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        rmax=max(r)
        print(rmax)
# look at the printed max values for the hight instibilaty

#%% P10.3.a
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from Lab 8 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points


# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(0-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

v0=1; #For ease we set this as one-half.
V=np.ones_like(x)*v0


# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    # we first define the following composites
    C1=-(tau/(8*h))*(V[j+1]+V[j+1]) # ASSUMING V IS CONSTANT IN TIME!!!!!!!!!!!
    C2=-(tau/(8*h))*(V[j-1]+V[j-1])
    A[j,j-1]=C2
    A[j,j]=1
    A[j,j+1]=-C1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    C1=-(tau/(8*h))*(V[j+1]+V[j+1]) # ASSUMING V IS CONSTANT IN TIME!!!!!!!!!!!
    C2=-(tau/(8*h))*(V[j-1]+V[j-1])
    B[j,j-1]=-C2
    B[j,j]=1
    B[j,j+1]=C1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5 # Set x=0 to one
A[0,1] = 0.5
A[-1,-1] = -1 #let x=L run free
A[-1,-2] = 1
A[-1,-3] = 1
A[-1,-4] = -1

# We now generate our initial conditions.
expo1=-200*(((x/L)-(1/4)))**2
rho = 1+np.exp(expo1) #copied from the text


j = 0
t = 0
tmax = 10
frames=tmax/tau
framestime=frames/10

#logging the times
framesmax=int(frames+1) # a modified version of times
times=np.linspace(0,tmax,framesmax) # ourtimesteps
logrho=np.zeros((N,framesmax))


plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t <= tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@rho
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 1 # We want the left end to remain at one
    r[-1] = 0
    
    # Solve A*rho = r. The rho we get is for the next time step.
    # We don't need to keep track of previous rho values, so just
    # load the new rho directly into rho itself
    rho = la.solve(A,r)
    
    # And log the rho
    logrho[0:,j-1]=rho
    
    if j % framestime == 0:
        plt.clf() # clear the figure window
        plt.plot(x,rho,'b')
        plt.xlabel('x')
        plt.ylabel('rho')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,2.5])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw

X,T = np.meshgrid(x,times,indexing='ij')

plt.figure(6)
plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,T,logrho, cmap=cm.plasma)
ax.set_zlim(0, 2)
ax.set_ylim(0,10)
ax.set_xlim(0,10)
plt.xlabel('x')
plt.ylabel('t')
ax.view_init(elev=30., azim=280.)
plt.draw()

#%% P10.3.b
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from Lab 8 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points


# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(0-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

V=1.2-(x/L) # THIS PART IS DIFFERENT


# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    # we first define the following composites
    C1=-(tau/(8*h))*(V[j+1]+V[j+1]) # ASSUMING V IS CONSTANT IN TIME!!!!!!!!!!!
    C2=-(tau/(8*h))*(V[j-1]+V[j-1])
    A[j,j-1]=C2
    A[j,j]=1
    A[j,j+1]=-C1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    C1=-(tau/(8*h))*(V[j+1]+V[j+1]) # ASSUMING V IS CONSTANT IN TIME!!!!!!!!!!!
    C2=-(tau/(8*h))*(V[j-1]+V[j-1])
    B[j,j-1]=-C2
    B[j,j]=1
    B[j,j+1]=C1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5 # Set x=0 to one
A[0,1] = 0.5
A[-1,-1] = -1 #let x=L run free
A[-1,-2] = 1
A[-1,-3] = 1
A[-1,-4] = -1

# We now generate our initial conditions.
expo1=-200*(((x/L)-(1/4)))**2
rho = 1+np.exp(expo1) #copied from the text


j = 0
t = 0
tmax = 10
frames=tmax/tau
framestime=frames/10

#logging the times
framesmax=int(frames+1) # a modified version of times
times=np.linspace(0,tmax,framesmax) # ourtimesteps
logrho=np.zeros((N,framesmax))



plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t <= tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@rho
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 1 # We want the left end to remain at one
    r[-1] = 0
    
    # Solve A*rho = r. The rho we get is for the next time step.
    # We don't need to keep track of previous rho values, so just
    # load the new rho directly into rho itself
    rho = la.solve(A,r)
    
    # And log the rho
    logrho[0:,j-1]=rho
    
    if j % framestime == 0:
        plt.clf() # clear the figure window
        plt.plot(x,rho,'b')
        plt.xlabel('x')
        plt.ylabel('rho')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,10])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
X,T = np.meshgrid(x,times,indexing='ij')

plt.figure(6)
plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,T,logrho, cmap=cm.plasma)
ax.set_zlim(0,10)
ax.set_ylim(0,10)
ax.set_xlim(0,10)
plt.xlabel('x')
plt.ylabel('t')
ax.view_init(elev=20., azim=250.)
plt.draw()

#%% P10.3.c
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# We now reuse our code from Lab 8 to use CN to solve our particle in a box.

# First, we define our constants
# -------------------- THIS PART IS DIFFERENT
# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points


# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(0-(h/2),L+(h/2),N) 

#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)

v0=1; #For ease we set this as one.
V=np.ones_like(x)*v0


# We Then use the snippit of code from the textbook
A = np.zeros((N,N),dtype=np.complex_)
B = np.zeros_like(A,dtype=np.complex_)


# We first define A ------------------------------------------------
for j in range(1,N-1,1):
    # we first define the following composites
    C1=-(tau/(8*h))*(V[j+1]+V[j+1]) # ASSUMING V IS CONSTANT IN TIME!!!!!!!!!!!
    C2=-(tau/(8*h))*(V[j-1]+V[j-1])
    A[j,j-1]=C2
    A[j,j]=1
    A[j,j+1]=-C1
    
# And now define B -------------------------------------------------
for j in range(1,N-1,1):
    C1=-(tau/(8*h))*(V[j+1]+V[j+1]) # ASSUMING V IS CONSTANT IN TIME!!!!!!!!!!!
    C2=-(tau/(8*h))*(V[j-1]+V[j-1])
    B[j,j-1]=-C2
    B[j,j]=1
    B[j,j+1]=C1
    
#And set the boundry conditions (in this case, x=0 at boundaries)
A[0,0] = 0.5 # Set x=0 to one
A[0,1] = 0.5
A[-1,-1] = -1 #let x=L run free
A[-1,-2] = 1
A[-1,-3] = 1
A[-1,-4] = -1

# We now generate our initial conditions.
rho=np.zeros_like(x)
end1=int(N/2)+1
rho[0:end1]=1

j = 0
t = 0
tmax = 10
frames=tmax/tau
framestime=frames/10

#logging the times
framesmax=int(frames+1) # a modified version of times
times=np.linspace(0,tmax,framesmax) # ourtimesteps
logrho=np.zeros((N,framesmax))


plt.figure(5) # Open the figure window

# the loop that steps the solution along
while t <= tmax:
    j = j+1
    t = t + tau
    
    # matrix multiply to get the right-hand side
    r = B@rho
    
    # set r as appropriate for the boundary conditions
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    r[0] = 1 # We want the left end to remain at one
    r[-1] = 0
    
    # Solve A*rho = r. The rho we get is for the next time step.
    # We don't need to keep track of previous rho values, so just
    # load the new rho directly into rho itself
    rho = la.solve(A,r)
    
    # And log the rho
    logrho[0:,j-1]=rho
    
    if j % framestime == 0:
        plt.clf() # clear the figure window
        plt.plot(x,rho,'b')
        plt.xlabel('x')
        plt.ylabel('rho')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,2.5])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw

X,T = np.meshgrid(x,times,indexing='ij')

plt.figure(6)
plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,T,logrho, cmap=cm.plasma)
ax.set_zlim(0, 2)
plt.xlabel('x')
plt.ylabel('t')
ax.view_init(elev=10., azim=90.)
plt.draw()

#%% P10.3.d--Lets try the earlier method
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=400 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=10 #length
N=400 # negative points

#we want to be able to define our own tau
tin=input("What value would you like for tau? ")
tau=float(tin)

#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N-1,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid

x=np.linspace(0-(h/2),L+(h/2),N) #this is the actual center-cell grid with 2 ghost points
#--0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0-0-0-0--0-0-0-0-0-0-0-0-0-0-0-0

# We now generate our initial conditions.
# We now generate our initial conditions.
r=np.zeros_like(x)
end1=int(N/2)+1
r[0:end1]=1

# and the initial velocity
v0=1
v=np.ones_like(x)*v0 # We Assume v0 to be constant

#------------------
#QUESTION?  WHY DOESNT V CHANGE OVER TIME

# WE DONT NEED A BACK STEP!

rnew = np.zeros_like(r)
j = 0
t = 0
tmax = 20
plt.figure(1) # Open the figure window

# one last thing: we define our weights
weight=tau/(2*h)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    rnew[1:-1]=r[1:-1]+weight*(r[0:-2]*v[0:-2]-r[2:]*v[2:])
    rnew[0]=2-rnew[1] # setting the boundary condition at x=0 to be 1
    rnew[-1]=rnew[-2]+rnew[3]-rnew[-4] # boundary conditions from the book
    
    #we now update yold and y
    rold=np.copy(r)
    r=np.copy(rnew)
    
    if j % 20 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,r,'b-')
        plt.xlabel('x')
        plt.ylabel('r')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([0,2])
        plt.xlim([0,10])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
# This still doesn't seem to work
#%% TEST SPACE
# Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

L=10 #length
N=400 # negative points


# this is a cell-edge grid used to gernerate the center cell grid
grid,h=np.linspace(0,L,N-1,retstep=True) 

# this is the actual center-cell grid with 2 ghost ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````
x=np.linspace(0-(h/2),L+(h/2),N) 

rho=np.zeros_like(x)
end1=int(N/2)+1
rho[0:end1]=1

plt.figure(7)
plt.plot(x,rho,'b')
plt.xlabel('x')
plt.ylabel('rho')
plt.title('test time')
plt.ylim([0,2.5])
plt.xlim([0,10])





