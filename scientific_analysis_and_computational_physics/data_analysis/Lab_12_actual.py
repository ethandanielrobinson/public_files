# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:22:13 2023

@author: ethan
"""

#%% LAB 12
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%%
# IMPORTANT NOTE
# THE LOG FLUME AT LAGOON IS BORING, AND RATTLE SNAKE RAPIDS IS MUCH BETTER
# AS IS SPLASH MOUNTAIN, FOR THAT MATTER.
#%% P12.1
# See Handwritten Notes
#%% P12.2
# See Handwritten Notes
#%% P12.3.a
# The code for problem 3 was taken from kdf.py and pasted here
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)

# Initial Gaussian centered on the computing region
ymax = 2
y = ymax * np.exp(-(x-.5*L)**2)

# Time range
tau = 0.5
tfinal = 100
t = np.arange(0,tfinal,tau)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 1
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(0,3)
        plt.pause(.1)
        
# Turns to garbage about 30 seconds in.
#%% P12.3.b
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)

# Initial Gaussian centered on the computing region
ymax = 2
y = ymax * np.exp(-(x-.5*L)**2)

# Time range
# THIS PART I ADDED FOR EASE OF USE--------------
# Generaly easier if i can just define my own tau
tin=input("What value would you like for tau? About 0.1 should do: ")
tau=float(tin)
#-------------
tfinal = 10
t = np.arange(0,tfinal,tau)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 10
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(0,3)
        plt.pause(.1)

#%% P13.4.a
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)

# Initial Gaussian centered on the computing region
ymax = 0.001
y = ymax * np.exp(-(x-.5*L)**2)

# Time range
tau = 0.1
tfinal = 10
t = np.arange(0,tfinal,tau)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 10
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(-0.001,0.002)
        plt.pause(.1)

#%% P12.4.b
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)

# Initial Gaussian centered on the computing region
ymax = 2
y = ymax * np.exp(-(x-.5*L)**2)

# Time range
tau = 0.01
tfinal = 10
t = np.arange(0,tfinal,tau)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 10
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(0,3)
        plt.pause(.1)
#%% P12.5.a
# See Mathmatica Addendum
#%% 12.5.b
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1377410468319559
k=1.1 #for the initial conditions

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)
x0=L/2 #for the initial conditions

# Initial Gaussian centered on the computing region
ymax = 2
# NEW SOLITON INITIAL CONDISTIONS
y =(12*(k**2)*alpha)/(np.cosh(k*(x-x0))**2)

# Time range
tau = 0.1
tfinal = 100
t = np.arange(0,tfinal,tau)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 10
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(0,3)
        plt.pause(.1)

# No Interference
#%% P12.5.c
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1377410468319559
k=1.1 #for the initial conditions

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)
x0=L/2 #for the initial conditions

# Initial Gaussian centered on the computing region
ymax = 2
# NEW SOLITON INITIAL CONDISTIONS
y =(12*(k**2)*alpha)/(np.cosh(k*(x-x0))**2)

# Time range
tau = 0.1
tfinal = 100
t = np.arange(0,tfinal,tau)
hightlog=np.zeros_like(t)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 10
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp
    
    # and record the position of the peak
    hightlog[n]=np.argmax(y)

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)
    

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(0,3)
        plt.pause(.05)

# We write some quick code to examine the first pass of the soliton
# from x=5 to x=10 (before the x-position restarts)
speed=((hightlog+1)*h-5)[1:75]/t[1:75]
xtest=((hightlog+1)*h)[1:75]

#and we plot
plt.figure(2)
plt.plot(xtest,speed,'b') #Actual will be blue, calculated will be red dots
plt.title('P12.5.c')
plt.legend(['speed from x=5 to x=10'])
plt.xlabel('x')
plt.ylim(0,1)

# We should want about 0.666667 according the given equation
#%% P12.6
import matplotlib.pyplot as plt
import numpy as np
import scipy.linalg as la

# Physical constants
alpha = 0.1
k1=1.5
k2=2

# Make the grid
N = 500
L = 10
h = L/N
x = np.linspace(h/2,L-h/2,N)
x01=(1/4)*L
x02=(3/4)*L

# Initial Gaussian centered on the computing region
ymax = 2
y = (12*(k1**2)*alpha)/(np.cosh(k1*(x-x01))**2)+(12*(k2**2)*alpha)/(np.cosh(k2*(x-x02))**2)

# Time range
tau = 0.1
tfinal = 20
t = np.arange(0,tfinal,tau)

# Initialize the parts of the A and B matrices that
# do not depend on ybar and load them into At and Bt.
# Make them be sparse so the code will run fast.
At = np.zeros((N,N))
Bt = np.zeros((N,N))

# Function to wrap the column index
def jwrap(j):
    if (j < 0):
        return j + N
    if (j >= N):
        return j - N
    return j

# load the matrices with the terms that don't depend on ybar
h3 = h**3
for j in range(N):
    At[j,jwrap(j-1)] =-0.5*alpha/h3
    At[j,j]          = 0.5/tau + 1.5*alpha/h3
    At[j,jwrap(j+1)] = 0.5/tau - 1.5*alpha/h3
    At[j,jwrap(j+2)] = 0.5*alpha/h3

    Bt[j,jwrap(j-1)] = 0.5*alpha/h3
    Bt[j,j]          = 0.5/tau - 1.5*alpha/h3
    Bt[j,jwrap(j+1)] = 0.5/tau + 1.5*alpha/h3
    Bt[j,jwrap(j+2)] =-0.5*alpha/h3


plt.figure(1)
skip = 10
for n in range(len(t)):
    # Predictor step
    A = np.copy(At)
    B = np.copy(Bt)

    # load ybar, then add its terms to A and B
    ybar = np.copy(y)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the predictor solve
    r = B@y
    yp = la.solve(A,r)

    # corrector step
    A = np.copy(At)
    B = np.copy(Bt)

    # average current and predicted y values to correct ybar
    ybar=.5*(y+yp)
    for j in range(N):
        tmp = 0.25*(ybar[jwrap(j+1)] + ybar[j])/h
        A[j,j]          = A[j,j] - tmp
        A[j,jwrap(j+1)] = A[j,jwrap(j+1)] + tmp
        B[j,j]          = B[j,j] + tmp
        B[j,jwrap(j+1)] = B[j,jwrap(j+1)] - tmp

    # do the final corrected solve
    r = B@y
    y = la.solve(A,r)

    if (n % skip == 0):
        plt.clf()
        plt.plot(x,y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('time={:1.3f}'.format(t[n]))
        plt.ylim(0,6)
        plt.pause(.05)

#%% Test Area
test=(12*(k1**2)*alpha)/(np.cosh(k*(x-x01))**2)+(12*(k2**2)*alpha)/(np.cosh(k*(x-x02))**2)
xtest=((hightlog+1)*h)[1:75]

#and we plot
plt.figure(2)
plt.plot(x,test,'b') #Actual will be blue, calculated will be red dots
plt.title('P12.6')
plt.legend(['initial conditions'])
plt.xlabel('x')
plt.ylim(0,6)