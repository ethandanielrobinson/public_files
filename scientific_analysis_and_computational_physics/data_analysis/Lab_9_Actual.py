# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:45:07 2023

@author: ethan
"""

#%% LAB 9
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P9.1.a
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la


actual=0.567 #The actual answer
n=1  #iteration counter
# User input of the initial guess
gin=input("What value would you like for your guess? ")
guess=float(gin)

x1=guess
error=1  #Set a placeholder for our intial error
while error > 0.00001:
    x2=np.exp(-x1)
    error=abs(x1-x2) # The difference between the two sides
    x1=x2 #itteritive part
    n=n+1
    if n > 1000:
        break
        print('Error: Overflow') #Breaks the while loop if it iterates more than 1000 times
    
print('Our Final Answer is {}'.format(x1)) #prints out the final answer

#%% P9.1.b
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

# Now we work on the log function, which should not converge

n=1  #iteration counter
# User input of the initial guess
gin=input("What value would you like for your guess? ")
guess=float(gin)

x1=guess
error=1  #Set a placeholder for our intial error
while error > 0.00001:
    x2=-np.log(x1) # THIS PART IS DIFFERENT
    print(x2)
    error=abs(x1-x2) # The difference between the two sides
    x1=x2 #itteritive part
    n=n+1
    if n > 100:
        break
        print('Error: Overflow') #Breaks the while loop if it iterates more than 1000 times
    
print('Our Final Answer is {}'.format(x1)) #prints out the final answer

#As we can see, the answer does not converge

#%% P9.2
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Make the grid
xmin = 0
xmax = 2
Nx = 80
x,hx = np.linspace(xmin,xmax,Nx,retstep = True)
hx2 = hx**2
ymin = 0
ymax = 2
Ny = 40
y,hy = np.linspace(ymin,ymax,Ny,retstep = True)
hy2 = hy**2
X,Y = np.meshgrid(x,y,indexing='ij')

# Initialize potential
V = 0.5*np.ones_like(X)

# Enforce boundary conditions
V[:,0] = 0
V[:,-1] = 0
V[0,:] = 1
V[-1,:] = 1
# Allow possibility of charge distribution
rho = np.zeros_like(X)
# Iterate
denom = 2/hx2 + 2/hy2
fig = plt.figure(1)
for n in range(200):
    # make plots every few steps
    if n % 10 == 0:
        plt.clf()
        ax=plt.axes(projection='3d') #Updated Code----------------------------
        surf = ax.plot_surface(X,Y,V)
        ax.set_zlim(-0.1, 2)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.draw()
        plt.pause(0.1)
        
    # Iterate the solution
    for j in range(1,Nx-1):
        for k in range(1,Ny-1):
            V[j,k] = ( (V[j+1,k] + V[j-1,k])/hx2
            +(V[j,k+1] + V[j,k-1])/hy2
            +rho[j,k]) / denom

#%% P9.3
# See Handwritten Notes

#%% P9.4.a
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la


n=0  #iteration counter
# User input of the initial guess
gin=input("What value would you like for your guess? ")
guess=float(gin)

win=input("What value would you like for your omega? ")
w=float(win)

x1=guess
error=1  #Set a placeholder for our intial error
while error > 0.0001:
    x2=w*np.exp(-x1)+(1-w)*x1
    error=abs(x1-x2) # The difference between the two sides
    x1=x2 #itteritive part
    n=n+1
    if n > 1000:
        break
        print('Error: Overflow') #Breaks the while loop if it iterates more than 1000 times
    
print('Our Final Answer is {}'.format(x1)) #prints out the final answer

#%% P9.4.b
#Boilerplate
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.linalg as la

#I want to create a plot of various w values
points=np.zeros(100)
w=np.linspace(0,1,100) 

count=np.arange(0,100,1) #counter for for loop

# User input of the initial guess
gin=input("What value would you like for your guess? ")
guess=float(gin)

for j in count:
    n=0  #iteration counter
    error=1  #Set a placeholder for our intial error
    x1=guess
    while error > 0.0001:
        x2=w[j]*np.exp(-x1)+(1-w[j])*x1
        error=abs(x1-x2) # The difference between the two sides
        x1=x2 #itteritive part
        n=n+1
        if n > 1000:
            break
            print('Error: Overflow') #Breaks the while loop if it iterates more than 1000 times
    points[j]=n

plt.figure(1)
plt.plot(w,points,'g') #will be green
plt.title('P9.4.b')
plt.legend(['n'])
plt.xlabel('w')

# We need at least one iteration to actualy update the sigma term

#%% P9.5
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# First of all, we want to ask the user for a omega input
win=input("What value would you like for your omega? ")
w=float(win)

# Make the grid
xmin = -2
xmax = 2
Nx = 30
x,hx = np.linspace(xmin,xmax,Nx,retstep = True)
hx2 = hx**2
ymin = 0
ymax = 2
Ny = 30
y,hy = np.linspace(ymin,ymax,Ny,retstep = True)
hy2 = hy**2
X,Y = np.meshgrid(x,y,indexing='ij')

# Initialize potential
V = 0.5*np.ones_like(X)

# Enforce boundary conditions
V[:,0] = 0 # x-axis
V[:,-1] = 0 # x maximum
V[0,:] = 1 # y-axis
V[-1,:] = 1# y maximum
# Allow possibility of charge distribution
rho = np.zeros_like(X)
# Iterate
denom = 2/hx2 + 2/hy2
fig = plt.figure(1)

# Itialize the error value and the count
error=1
count=0;

while error > 0.0001 :
    temperror=0 # The changing error we will use to find the max error per iteration
    maxerror=0 #the maximum error per n
    Vscale=1 # The maximum V scale
    # Iterate the solution
    for j in range(1,Nx-1):
        for k in range(1,Ny-1):
            LHS=V[j,k] # Value of V[j,k] before iteration
            V[j,k] = w*( (V[j+1,k] + V[j-1,k])/hx2
            +(V[j,k+1] + V[j,k-1])/hy2
            +rho[j,k]) / denom + (1-w)*V[j,k]
            RHS=V[j,k]=V[j,k] # Value of V[j,k] after iteration
            if V[j,k] > Vscale:
                Vscale =V[j,k] #test for the value of Vscale
            temperror=abs((LHS-RHS)/Vscale)
            if temperror > maxerror:
                maxerror=temperror
    error=maxerror # Redefine error
    count=count+1

plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,Y,V)
ax.set_zlim(-0.1, 2)
plt.xlabel('x')
plt.ylabel('y')
plt.draw()

print('the error is {}'.format(error))
print('the count is {}'.format(count))

# According to problem 9.16, the best is w=1.81

#%% P9.6.a

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# We use the ideal w for our setup
w=1.81

# Make the grid
xmin = -2
xmax = 2
Nx = 30
x,hx = np.linspace(xmin,xmax,Nx,retstep = True)
hx2 = hx**2
ymin = 0
ymax = 2
Ny = 30
y,hy = np.linspace(ymin,ymax,Ny,retstep = True)
hy2 = hy**2
X,Y = np.meshgrid(x,y,indexing='ij')

# Initialize potential
V = 0.5*np.ones_like(X)

# Enforce boundary conditions
V[:,0] = 0 # x-axis
V[:,-1] = 0 # x maximum
V[0,:] = -1 # y-axis
V[-1,:] = 1# y maximum
# Allow possibility of charge distribution
rho = np.zeros_like(X)
# Iterate
denom = 2/hx2 + 2/hy2
fig = plt.figure(1)

# Itialize the error value and the count
error=1
count=0;

while error > 0.0001 :
    temperror=0 # The changing error we will use to find the max error per iteration
    maxerror=0 #the maximum error per n
    Vscale=1 # The maximum V scale
    # Iterate the solution
    for j in range(1,Nx-1):
        for k in range(1,Ny-1):
            LHS=V[j,k] # Value of V[j,k] before iteration
            V[j,k] = w*( (V[j+1,k] + V[j-1,k])/hx2
            +(V[j,k+1] + V[j,k-1])/hy2
            +rho[j,k]) / denom + (1-w)*V[j,k]
            RHS=V[j,k]=V[j,k] # Value of V[j,k] after iteration
            if V[j,k] > Vscale:
                Vscale =V[j,k] #test for the value of Vscale
            temperror=abs((LHS-RHS)/Vscale)
            if temperror > maxerror:
                maxerror=temperror
    error=maxerror # Redefine error
    count=count+1

plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,Y,V)
ax.set_zlim(-0.1, 2)
ax.view_init(elev=10., azim=120.)
plt.xlabel('x')
plt.ylabel('y')
plt.draw()

print('the error is {}'.format(error))
print('the count is {}'.format(count))

#%% P9.6.b

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# We use the ideal w for our setup
w=1.96
# 1.96 seems to work the best

# Make the grid
xmin = -2
xmax = 2
Nx = 30
x,hx = np.linspace(xmin,xmax,Nx,retstep = True)
hx2 = hx**2
ymin = 0
ymax = 2
Ny = 30
y,hy = np.linspace(ymin,ymax,Ny,retstep = True)
hy2 = hy**2
X,Y = np.meshgrid(x,y,indexing='ij')

# Initialize potential
V = 0.5*np.ones_like(X)

# temporary initial boundary conditions
V[:,0] = 0 # x-axis
V[:,-1] = 0 # x maximum
V[0,:] = 0 # y-axis
V[-1,:] = 1# y maximum
# Allow possibility of charge distribution
rho = np.zeros_like(X)
# Iterate
denom = 2/hx2 + 2/hy2
fig = plt.figure(1)

# Itialize the error value and the count
error=1
count=0;

while error > 0.0001 :
    temperror=0 # The changing error we will use to find the max error per iteration
    maxerror=0 #the maximum error per n
    Vscale=1 # The maximum V scale
    # Iterate the solution
    for j in range(1,Nx-1):
        for k in range(1,Ny-1):
            LHS=V[j,k] # Value of V[j,k] before iteration
            V[j,k] = w*( (V[j+1,k] + V[j-1,k])/hx2
            +(V[j,k+1] + V[j,k-1])/hy2
            +rho[j,k]) / denom + (1-w)*V[j,k]
            RHS=V[j,k]=V[j,k] # Value of V[j,k] after iteration
            if V[j,k] > Vscale:
                Vscale =V[j,k] #test for the value of Vscale
            temperror=abs((LHS-RHS)/Vscale)
            if temperror > maxerror:
                maxerror=temperror
                
    # Now We apply the relocated boundary conditions
    V[:,0] = 0 # y-minimum
    V[:,-1] = (1/3)*(4*V[:,-2]-V[:,-3]) # y maximum
    V[0,:] =  (1/3)*(4*V[1,:]-V[2,:])# x-minimum
    V[-1,:] = 1# x-maximum
    error=maxerror # Redefine error
    count=count+1

plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,Y,V)
ax.set_zlim(-0.1, 2)
ax.view_init(elev=10., azim=210.)
plt.xlabel('x')
plt.ylabel('y')
plt.draw()

print('the error is {}'.format(error))
print('the count is {}'.format(count))

#%% P9.6.c

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# We use the ideal w for our setup
w=1.81

# Make the grid
xmin = -2
xmax = 2
Nx = 30
x,hx = np.linspace(xmin,xmax,Nx,retstep = True)
hx2 = hx**2
ymin = 0
ymax = 2
Ny = 30
y,hy = np.linspace(ymin,ymax,Ny,retstep = True)
hy2 = hy**2
X,Y = np.meshgrid(x,y,indexing='ij')

# Initialize potential
V = 0.5*np.ones_like(X)

# Enforce boundary conditions
V[:,0] = 0 # x-axis
V[:,-1] = 0 # x maximum
V[0,:] = -1 # y-axis
V[-1,:] = 1# y maximum
# Allow possibility of charge distribution
rho = np.zeros_like(X)
# Iterate
denom = 2/hx2 + 2/hy2

# And create the mask
mask=np.ones_like(V)
# and create some grounded points
mask[5,9]=0
mask[5,14]=0
mask[5,19]=0
mask[14,9]=0
mask[14,14]=0
mask[14,19]=0
mask[25,9]=0
mask[25,14]=0
mask[25,19]=0

# Itialize the error value and the count
error=1
count=0;

while error > 0.0001 :
    temperror=0 # The changing error we will use to find the max error per iteration
    maxerror=0 #the maximum error per n
    Vscale=1 # The maximum V scale
    # Iterate the solution
    for j in range(1,Nx-1):
        for k in range(1,Ny-1):
            if mask[j,k] == 1:
                LHS=V[j,k] # Value of V[j,k] before iteration
                V[j,k] = w*( (V[j+1,k] + V[j-1,k])/hx2
                +(V[j,k+1] + V[j,k-1])/hy2
                +rho[j,k]) / denom + (1-w)*V[j,k]
                RHS=V[j,k]=V[j,k] # Value of V[j,k] after iteration
                if V[j,k] > Vscale:
                    Vscale =V[j,k] #test for the value of Vscale
                temperror=abs((LHS-RHS)/Vscale)
                if temperror > maxerror:
                    maxerror=temperror
            else:
                V[j,k]=0 # ensure that the points remain grounded
    error=maxerror # Redefine error
    count=count+1

fig = plt.figure(1)
plt.clf()
ax=plt.axes(projection='3d') #Updated Code----------------------------
surf = ax.plot_surface(X,Y,V, cmap=cm.plasma)
ax.set_zlim(-0.1, 2)
ax.view_init(elev=15., azim=140.)
plt.xlabel('x')
plt.ylabel('y')
plt.draw()

print('the error is {}'.format(error))
print('the count is {}'.format(count))
#%% TEST SPACE
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np



