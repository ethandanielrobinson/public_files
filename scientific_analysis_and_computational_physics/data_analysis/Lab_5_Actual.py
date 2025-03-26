# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 22:45:02 2023

@author: ethan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:00:52 2023

@author: ethan
"""

#%% ETHAN DANIEL ROBINSON
# PHSCS 430 LAB 5
# 28 SEPT 2023
#%% P5.1  See Handwritten Notes
#%% P5.2  See Handwritten Notes
#%% P5.3.a
# from there
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
L=1
N=200
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points

# We now generate our initial conditions.
y = 0.01 * np.exp(-(x-L/2)**2 / 0.02) #copied from the text
#and the initial velocity
v=np.zeros_like(x)

# TEST PLOT
plt.figure(1)
plt.plot(x,y,'b') #will be blue
plt.title('P5.3.a')
plt.xlabel('x')

#%% P5.3.b & & P5.3.c
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1
N=200
c=2
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
tau=0.2*h/c #coppied from the text

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points

# We now generate our initial conditions.
y = 0.01 * np.exp(-(x-L/2)**2 / 0.02) #copied from the text
# and the initial velocity
v=np.zeros_like(x)

# we now need to create our back-step, yold, using equation 5.11 in the text
# first, we initialize
yold=np.zeros_like(y)
modifier=((c**2)*(tau**2))/(2*(h**2)) #this is the nasty fraction before the second part of equation 5.11
yold[1:-1]=y[1:-1]-v[1:-1]*tau+modifier*(y[2:]-2*y[1:-1]+y[0:-2])  #assign all points simultaniously by shifting our domain
# we then set our boundary conditions
yold[0]=-yold[1]
yold[N+1]=-yold[N]

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 2
plt.figure(1) # Open the figure window

# one last thing: we define (c**2 tau**2/h**2) for ease of use
weight=((c**2)*(tau**2))/(h**2)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=2*y[1:-1]-yold[1:-1]+weight*(y[2:]-2*y[1:-1]+y[0:-2])
    ynew[0]=-ynew[1] # setting the boundary condition at x=0 to be 0
    ynew[-1]=-ynew[-2] # setting the boundary condition at x=L to be 0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.03,0.03])
        plt.xlim([0,1])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
#%% P5.3.d
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1
N=200
c=2
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
# THIS PART IS  DIFFERENT
tauin=input('what would you like the weight of tau to be against h/c? ')
tauw=float(tauin)
tau=tauw*h/c #coppied from the text

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points

# We now generate our initial conditions.
y = 0.01 * np.exp(-(x-L/2)**2 / 0.02) #copied from the text
# and the initial velocity
v=np.zeros_like(x)

# we now need to create our back-step, yold, using equation 5.11 in the text
# first, we initialize
yold=np.zeros_like(y)
modifier=((c**2)*(tau**2))/(2*(h**2)) #this is the nasty fraction before the second part of equation 5.11
yold[1:-1]=y[1:-1]-v[1:-1]*tau+modifier*(y[2:]-2*y[1:-1]+y[0:-2])  #assign all points simultaniously by shifting our domain
# we then set our boundary conditions
yold[0]=-yold[1]
yold[N+1]=-yold[N]

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 2
plt.figure(1) # Open the figure window

# one last thing: we define (c**2 tau**2/h**2) for ease of use
weight=((c**2)*(tau**2))/(h**2)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=2*y[1:-1]-yold[1:-1]+weight*(y[2:]-2*y[1:-1]+y[0:-2])
    ynew[0]=-ynew[1] # setting the boundary condition at x=0 to be 0
    ynew[-1]=-ynew[-2] # setting the boundary condition at x=L to be 0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.03,0.03])
        plt.xlim([0,1])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
#%% P5.3.e
# We now recreate the same code, but allow the user to input our tau weight
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1
N=200
c=2
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
tau=0.2*h/c #coppied from the text

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points

# We now generate our initial conditions.
y = 0.01 * np.exp(-(x-L/2)**2 / 0.02) #copied from the text
# and the initial velocity
v=np.zeros_like(x)

# we now need to create our back-step, yold, using equation 5.11 in the text
# first, we initialize
yold=np.zeros_like(y)
modifier=((c**2)*(tau**2))/(2*(h**2)) #this is the nasty fraction before the second part of equation 5.11
yold[1:-1]=y[1:-1]-v[1:-1]*tau+modifier*(y[2:]-2*y[1:-1]+y[0:-2])  #assign all points simultaniously by shifting our domain
# we then set our boundary conditions
# THIS PART IS DIFFERENT
yold[0]=yold[1]
yold[N+1]=yold[N]

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 2
plt.figure(1) # Open the figure window

# one last thing: we define (c**2 tau**2/h**2) for ease of use
weight=((c**2)*(tau**2))/(h**2)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=2*y[1:-1]-yold[1:-1]+weight*(y[2:]-2*y[1:-1]+y[0:-2])
    #THIS PART IS DIFFERENT
    ynew[0]=ynew[1] # setting the boundary condition at x=0 to be v=0
    ynew[-1]=ynew[-2] # setting the boundary condition at x=L to be v=0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.03,0.03])
        plt.xlim([0,1])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
#%% P5.3.f
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1
N=200
c=2
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
tau=0.2*h/c #coppied from the text

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points

# THIS PART IS DIFFERENT------------------------------------------------------
# We now generate our initial conditions.
y = np.zeros_like(x)
# and the initial velocity
v=0.01 * np.exp(-(x-L/2)**2 / 0.02) #copied from the text

# we now need to create our back-step, yold, using equation 5.11 in the text
# first, we initialize
yold=np.zeros_like(y)
modifier=((c**2)*(tau**2))/(2*(h**2)) #this is the nasty fraction before the second part of equation 5.11
yold[1:-1]=y[1:-1]-v[1:-1]*tau+modifier*(y[2:]-2*y[1:-1]+y[0:-2])  #assign all points simultaniously by shifting our domain
# we then set our boundary conditions
yold[0]=-yold[1]
yold[N+1]=-yold[N]

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 2
plt.figure(1) # Open the figure window

# one last thing: we define (c**2 tau**2/h**2) for ease of use
weight=((c**2)*(tau**2))/(h**2)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=2*y[1:-1]-yold[1:-1]+weight*(y[2:]-2*y[1:-1]+y[0:-2])
    ynew[0]=-ynew[1] # setting the boundary condition at x=0 to be 0
    ynew[-1]=-ynew[-2] # setting the boundary condition at x=L to be 0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    if j % 50 == 0:
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.003,0.003])
        plt.xlim([0,1])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
#%% P5.4.a  SEE NOTES
#%% P5.4.b  SEE NOTES
#%% P5.4.c
# We reutilize some of our code from P5.3.f, but we have a new leapfrog function.
# For this to work best, we need to utilize the folowing constants
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1
N=200
c=2
gamma=0.2 #gamma value------
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
tau=0.9*h/c #coppied from the text

#the folowing defined constants will be used regularly in our code
const1=1/(2+(gamma*tau)) #1/(2+g*t)
const2=(gamma*tau)-2 #(g*t-2)
const3=(2*(tau**2)*(gamma**2))/(h**2) #(2*t^2*c^2/h^2)
const4=tau+((gamma*(tau**2))/2) #(t+(g*t^2)/2)
const5=((tau**2)*(gamma**2))/(2*(h**2)) #(t^2*c^2)/(2*h^2)

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points

# THIS PART IS DIFFERENT------------------------------------------------------
# We now generate our initial conditions.
y = np.zeros_like(x)
# and the initial velocity
v=0.01 * np.exp(-(x-L/2)**2 / 0.02) #copied from the text

# we now need to create our back-step, yold, using equation 5.11 in the text
# first, we initialize
yold=np.zeros_like(y)
yold[1:-1]=y[1:-1]-const4*v[1:-1]+const5*(y[2:]-2*y[1:-1]+y[0:-2])  #assign all points simultaniously by shifting our domain
# we then set our boundary conditions
yold[0]=-yold[1]
yold[N+1]=-yold[N]

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 25 #Increased time duration
plt.figure(1) # Open the figure window

#We now create a array to store the maximum y values
jmax=49750
amp=np.zeros(jmax) #this is the maximum number of j
times=np.zeros(jmax)

# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=const1*(4*y[1:-1]+const2*yold[1:-1]+const3*(y[2:]-2*y[1:-1]+y[0:-2]))
    ynew[0]=-ynew[1] # setting the boundary condition at x=0 to be 0
    ynew[-1]=-ynew[-2] # setting the boundary condition at x=L to be 0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    #and record the maximum value of y
    ymax=max(np.abs(y))
    amp[j-1]=ymax
    times[j-1]=t
    
    if j % 500 == 0: #Increased draw gaps
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.01,0.01])
        plt.xlim([0,1])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
#%% P5.4.c cont.
#We now want to plot the maximum ampltudes
jlist=np.arange(0,jmax)

#plot our comparison function
real=0.0065*np.exp(-(gamma*times)/2)

# and plot
plt.figure(10)
plt.plot(times,amp,'b',times,real,"r") #will be blue
plt.title('P5.4.c')
plt.legend(['ymax'])
plt.xlabel('time')

#%% P5.5.a SEE NOTES
#%% P5.5.b
# Modified code from part 4
# For this to work best, we need to utilize the folowing constants
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1.2
N=200
T=127
mu=0.003
omega=400 #our Driving frequency
cin=T/mu
c=np.sqrt(cin)
gin=input('what would you like the value of gamma to be?  ')
gamma=float(gin) #gamma value------
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
tau=0.2*h/c #coppied from the text

#the folowing defined constants will be used regularly in our code
const1=1/(2+(gamma*tau)) #1/(2+g*t)
const2=(gamma*tau)-2 #(g*t-2)
const3=(2*(tau**2)*(gamma**2))/(h**2) #(2*t^2*c^2/h^2)
const4=(2*(tau**2))/mu

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points


# We now generate our initial conditions of a string at rest.
y = np.zeros_like(x)
yold=np.zeros_like(y)

# and bring in our driving function from P3.2.a
#  We need to find the appropriate indicies for
# x=0.8 and x=1
j1=int(0.8/h)
j2=int(1/h)
f=np.zeros_like(x)
f[j1:j2]=0.73

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 25 #Increased time duration
plt.figure(1) # Open the figure window


# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=const1*(4*y[1:-1]+const2*yold[1:-1]+const3*(y[2:]-2*y[1:-1]+y[0:-2])+const4*f[1:-1]*np.cos(omega*t))
    ynew[0]=-ynew[1] # setting the boundary condition at x=0 to be 0
    ynew[-1]=-ynew[-2] # setting the boundary condition at x=L to be 0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    if j % 100000 == 0: #Increased draw gaps
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.005,0.005])
        plt.xlim([0,L])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw
        
#%% P5.5.b.ii
# Modified code from part 4
# For this to work best, we need to utilize the folowing constants
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps

# We then create a N=200 center-cell grid with ghost points
# Define Global Variables-----------------------------------------------------
L=1.2
N=200
T=127
mu=0.003
omega=1080 #our Driving frequency
cin=T/mu
c=np.sqrt(cin)
gin=input('what would you like the value of gamma to be?  ')
gamma=float(gin) #gamma value------
#-----------------------------------------------------------------------------
grid,h=np.linspace(0,L,N,retstep=True) #this is a cell-edge grid used to gernerate the center cell grid
tau=0.2*h/c #coppied from the text

#the folowing defined constants will be used regularly in our code
const1=1/(2+(gamma*tau)) #1/(2+g*t)
const2=(gamma*tau)-2 #(g*t-2)
const3=(2*(tau**2)*(gamma**2))/(h**2) #(2*t^2*c^2/h^2)
const4=(2*(tau**2))/mu

x=np.linspace(0-(h/2),L+(h/2),N+2) #this is the actual center-cell grid with 2 ghost points


# We now generate our initial conditions of a string at rest.
y = np.zeros_like(x)
yold=np.zeros_like(y)

# and bring in our driving function from P3.2.a
#  We need to find the appropriate indicies for
# x=0.8 and x=1
j1=int(0.8/h)
j2=int(1/h)
f=np.zeros_like(x)
f[j1:j2]=0.73

ynew = np.zeros_like(y)
j = 0
t = 0
tmax = 25 #Increased time duration
plt.figure(1) # Open the figure window


# the loop that steps the solution along
while t < tmax:
    j = j+1
    t = t + tau
    
    #We Now Begin our Leapfrog Code
    ynew[1:-1]=const1*(4*y[1:-1]+const2*yold[1:-1]+const3*(y[2:]-2*y[1:-1]+y[0:-2])+const4*f[1:-1]*np.cos(omega*t))
    ynew[0]=-ynew[1] # setting the boundary condition at x=0 to be 0
    ynew[-1]=-ynew[-2] # setting the boundary condition at x=L to be 0
    
    #we now update yold and y
    yold=np.copy(y)
    y=np.copy(ynew)
    
    if j % 10000 == 0: #Increased draw gaps
        plt.clf() # clear the figure window
        plt.plot(x,y,'b-')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t))
        plt.ylim([-0.005,0.005])
        plt.xlim([0,L])
        plt.draw() # Draw the plot
        plt.pause(0.1) # Give the computer time to draw






