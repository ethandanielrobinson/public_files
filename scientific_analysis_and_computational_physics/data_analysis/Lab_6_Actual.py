# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 18:48:46 2023

@author: ethan
"""

#%% LAB 6
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P6.1.a
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# Make 1D x and y arrays--We made sure to modify the grid to the correct parameters
Nx=30
a=0
b=2
x,hx = np.linspace(a,b,Nx,retstep = True)
Ny=50
c=-1
d=3
y,hy = np.linspace(c,d,Ny,retstep = True)

# Make the 2D grid and evaluate a function
X, Y = np.meshgrid(x,y,indexing='ij') #changing to xy swaps the rows and columns in the X and Y matricies
Z = X**2 + Y**2

# Plot the function as a surface.
fig = plt.figure(1)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis)
plt.xlabel('x')
plt.ylabel('y')
fig.colorbar(surf)

#%% P6.1.b
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# Make 1D x and y arrays--We made sure to modify the grid to the correct parameters
Nx=30
a=0
b=2
x,hx = np.linspace(a,b,Nx,retstep = True)
Ny=50
c=-1
d=3
y,hy = np.linspace(c,d,Ny,retstep = True)

# Make the 2D grid and evaluate a function
X, Y = np.meshgrid(x,y,indexing='ij')
#THIS IS OUR NEW SURFACE
Z = np.exp(-((X**2)+(Y**2)))*np.cos(5*np.sqrt((X**2)+(Y**2)))

# Plot the function as a surface.
fig = plt.figure(2)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis)
plt.xlabel('x')
plt.ylabel('y')
fig.colorbar(surf)

#%% P6.2.a
# First, some code that I took from the workbook
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

#Then, my own code to intialize things----------------------------------------

#First, we want to create our inital grid
# Make 1D x and y arrays--We made sure to modify the grid to the correct parameters
# of 101 points
N=101
a=-5
b=5
x,h = np.linspace(a,b,N,retstep = True)
y=np.copy(x) # We want a square


# Make the 2D grid
X, Y = np.meshgrid(x,y,indexing='ij')


# We now define some constants
sigma=2
mu=0.3
tau=0.01 # I chose 0.1 seconds for tau to start
const1=(sigma*(tau**2))/(mu*(h**2)) #These last two constants are used in the leapfrog function.
const2=0.5*const1

# We now define our inital conditions, with modified code from lab 5
Z = np.exp(-5*((X**2)+(Y**2))) #We evaluate the exponential spike
# and pin the edges to zero
Z[0:N,0]=0 #Left
Z[0:N,N-1]=0 #Right
Z[0,0:N]=0 #Top
Z[N-1,0:N]=0 #Bottom
# and the initial velocity
V0=np.zeros_like(Z)

# we now need to create our back-step,Zold, using equation 5.11 in the text
# first, we initialize
Zold=np.zeros_like(Z)
# Then Generate
# remember, we don't need to worry about the edge points (since they are pinned to zero)
# so our function can run just over the interior points.
Zold[1:-1,1:-1]=Z[1:-1,1:-1]-(tau*V0[1:-1,1:-1])+const2*(Z[2:,1:-1]+Z[0:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,0:-2]-4*(Z[1:-1,1:-1]))


Znew = np.zeros_like(Z)

#-----------------------------------------------------------------------------
#Back to code I coppied
tfinal=10
t=np.arange(0,tfinal,tau)
skip=10 #Sorry, I had to change this
fig = plt.figure(3)

storage=np.zeros((N,N,10))
s=0
# here is the loop that steps the solution along
for m in range(len(t)):
    
    # Your code to step the solution
    #--------------------------------------------------------------------------
    # once again, we can only worry about the interior points, since our boundary
    # conditions pin the edges to zero
    Znew[1:-1,1:-1]=2*Z[1:-1,1:-1]-Zold[1:-1,1:-1]+const1*(Z[2:,1:-1]+Z[0:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,0:-2]-4*(Z[1:-1,1:-1]))
    
    # And advance the leapfrog program
    Zold=np.copy(Z)
    Z=np.copy(Znew)
    
    #find the maximum
    Zmax=np.amax(np.abs(Z))
    #--------------------------------------------------------------------------
    if m % skip == 0:
        plt.clf()
        ax=plt.axes(projection='3d')
        surf = ax.plot_surface(X, Y, Z)
        ax.set_zlim(-0.5, 0.5)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.draw()
        plt.pause(0.1)

#%% P6.2.b
# First, some code that I took from the workbook
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

#Then, my own code to intialize things----------------------------------------

#First, we want to create our inital grid
# Make 1D x and y arrays--We made sure to modify the grid to the correct parameters
# of 101 points
N=101
a=-5
b=5
x,h = np.linspace(a,b,N,retstep = True)
y=np.copy(x) # We want a square


# Make the 2D grid
X, Y = np.meshgrid(x,y,indexing='ij')


# We now define some constants
sigma=2
mu=0.3
#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)
const1=(sigma*(tau**2))/(mu*(h**2)) #These last two constants are used in the leapfrog function.
const2=0.5*const1

# We now define our inital conditions, with modified code from lab 5
Z = np.exp(-5*((X**2)+(Y**2))) #We evaluate the exponential spike
# and pin the edges to zero
Z[0:N,0]=0 #Left
Z[0:N,N-1]=0 #Right
Z[0,0:N]=0 #Top
Z[N-1,0:N]=0 #Bottom
# and the initial velocity
V0=np.zeros_like(Z)

# we now need to create our back-step,Zold, using equation 5.11 in the text
# first, we initialize
Zold=np.zeros_like(Z)
# Then Generate
# remember, we don't need to worry about the edge points (since they are pinned to zero)
# so our function can run just over the interior points.
Zold[1:-1,1:-1]=Z[1:-1,1:-1]-(tau*V0[1:-1,1:-1])+const2*(Z[2:,1:-1]+Z[0:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,0:-2]-4*(Z[1:-1,1:-1]))


Znew = np.zeros_like(Z)

#-----------------------------------------------------------------------------
#Back to code I coppied
tfinal=10
t=np.arange(0,tfinal,tau)
skip=10 #Sorry, I had to change this
fig = plt.figure(3)

storage=np.zeros((N,N,10))
s=0

# for part c
center=np.zeros_like(t)

# here is the loop that steps the solution along
for m in range(len(t)):
    
    # Your code to step the solution
    #--------------------------------------------------------------------------
    # once again, we can only worry about the interior points, since our boundary
    # conditions pin the edges to zero
    Znew[1:-1,1:-1]=2*Z[1:-1,1:-1]-Zold[1:-1,1:-1]+const1*(Z[2:,1:-1]+Z[0:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,0:-2]-4*(Z[1:-1,1:-1]))
    
    # And advance the leapfrog program
    Zold=np.copy(Z)
    Z=np.copy(Znew)
    
    #find the maximum
    Zmax=np.amax(np.abs(Z))
    
    #this is for part c
    center[m]=Z[50,50] #which is the equilant of point (0,0)
    
    #--------------------------------------------------------------------------
    if m % skip == 0:
        plt.clf()
        ax=plt.axes(projection='3d')
        surf = ax.plot_surface(X, Y, Z)
        ax.set_zlim(-0.5, 0.5)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.draw()
        plt.pause(0.05)

#f is apx 0.645497
#%% P6.2.c

plt.figure(8)
plt.plot(t,center,'b') #will be blue
plt.title('P6.2.c')
plt.xlabel('t')

#it actulay drops below zero

#%% P6.2.d
# First, some code that I took from the workbook
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

#Then, my own code to intialize things----------------------------------------

#First, we want to create our inital grid
# Make 1D x and y arrays--We made sure to modify the grid to the correct parameters
# of 101 points
N=101
a=-5
b=5
x,h = np.linspace(a,b,N,retstep = True)
y=np.copy(x) # We want a square


# Make the 2D grid
X, Y = np.meshgrid(x,y,indexing='ij')


# We now define some constants
sigma=2
mu=0.3
#---------------- WE WANT TO BE ABLE TO DEFINE OUR OWN TAU
tin=input("What value would you like for tau? ")
tau=float(tin)
const1=(sigma*(tau**2))/(mu*(h**2)) #These last two constants are used in the leapfrog function.
const2=0.5*const1

# We now define our inital conditions, with modified code from lab 5
Z = np.zeros_like(Z)#We evaluate the exponential spike
# and pin the edges to zero

# and the initial velocity
V0=np.exp(-5*((X**2)+(Y**2)))
V0[0:N,0]=0 #Left
V0[0:N,N-1]=0 #Right
V0[0,0:N]=0 #Top
V0[N-1,0:N]=0 #Bottom

# we now need to create our back-step,Zold, using equation 5.11 in the text
# first, we initialize
Zold=np.zeros_like(Z)
# Then Generate
# remember, we don't need to worry about the edge points (since they are pinned to zero)
# so our function can run just over the interior points.
Zold[1:-1,1:-1]=Z[1:-1,1:-1]-(tau*V0[1:-1,1:-1])+const2*(Z[2:,1:-1]+Z[0:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,0:-2]-4*(Z[1:-1,1:-1]))


Znew = np.zeros_like(Z)

#-----------------------------------------------------------------------------
#Back to code I coppied
tfinal=10
t=np.arange(0,tfinal,tau)
skip=10 #Sorry, I had to change this
fig = plt.figure(3)

storage=np.zeros((N,N,10))
s=0

# for part c
center=np.zeros_like(t)

# here is the loop that steps the solution along
for m in range(len(t)):
    
    # Your code to step the solution
    #--------------------------------------------------------------------------
    # once again, we can only worry about the interior points, since our boundary
    # conditions pin the edges to zero
    Znew[1:-1,1:-1]=2*Z[1:-1,1:-1]-Zold[1:-1,1:-1]+const1*(Z[2:,1:-1]+Z[0:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,0:-2]-4*(Z[1:-1,1:-1]))
    
    # And advance the leapfrog program
    Zold=np.copy(Z)
    Z=np.copy(Znew)
    
    #find the maximum
    Zmax=np.amax(np.abs(Z))
    
    #this is for part c
    center[m]=Z[50,50] #which is the equilant of point (0,0)
    
    #--------------------------------------------------------------------------
    if m % skip == 0:
        plt.clf()
        ax=plt.axes(projection='3d')
        surf = ax.plot_surface(X, Y, Z)
        ax.set_zlim(-0.1, 0.1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.draw()
        plt.pause(0.05)
