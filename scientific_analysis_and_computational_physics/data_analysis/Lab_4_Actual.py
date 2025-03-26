# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 21:00:52 2023

@author: ethan
"""

#%% ETHAN DANIEL ROBINSON
# PHSCS 430 LAB 4
# 21 SEPT 2023

#%% P4.1  The hanging chain, part I--See handwriten notes

#%% P4.2 The hanginng chain, part II
# for parts A and B see notes
# P4.2.c
#-----------------------------------------------------------------------------
# Since we are going to be using the same method as P3.3, we reproduce our code
# from there
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps
# We write a program to numerically find the eigenvalues and eigenvectors
# We first start by defining a centered cell grid with ghost points

# We start by defining our global variables
# We have a 2 meter long chain
L=2
g=9.8 #
N=201 #we want our grid to have 200 cells.  That means we will end up with 202 data points in our
# cell centered grid with ghost points

# We then create a cell-edge grid as an intermediate step
grid,h=np.linspace(0,L,N,retstep=True)

gap=0.5*h #this isthe overhang between our cells and our ghost points

#we now create our points in ghost cell grid
x=np.linspace(0-gap,L+gap,N+1)

# We next need our vectors, A and B.
# A is easy enough, with code borrowed from lab 2
#And form the A matrix (coppied from lab 2)
A=np.zeros((N+1,N+1))
for n in range(1,N,1):
    A[n,n-1]=(x[n]/(h**2))-(1/(2*h))
    A[n,n]=-((2*x[n])/(h**2))
    A[n,n+1]=(x[n]/(h**2))+(1/(2*h))
    
#Then we set the boundary conditions
A[0,0]=-1/h
A[0,1]=1/h
A[N,N]=1/2 #bottom right corner, point (201,201)
A[N,N-1]=1/2 #(201,200)

#Similarly for B (which allows us to model more complex boundary conditions)
B=np.identity(N+1)
B[0,0]=1/2
B[0,1]=1/2
B[N,N]=0

#Then, we solve
# we then use pythons built-in generalized eigenvalue function
vals,vecs=la.eig(A,B)
# As we expect we get two infinite eigenvalues.

# We wish to compute the eigen-frequencies, however
w=np.sqrt(-g*np.real(vals))

# and to sort the eigenvalues and eigenvectors
ind=np.argsort(w)
w=w[ind]
vecs=vecs[:,ind]

print(f'the calculated first 3 values are {w[0:3]}')

# we plot the first few modes
eigen1=vecs[0:N+1,0]
eigen2=vecs[0:N+1,1]
eigen3=vecs[0:N+1,2]

# and plot
plt.figure(1)
plt.plot(eigen1,x,'b') #will be blue
plt.title('P4.2.c.i')
plt.legend(['n=1'])
plt.ylabel('x')

plt.figure(2)
plt.plot(eigen2,x,'b') #will be blue
plt.title('P4.2.c.ii')
plt.legend(['n=2'])
plt.ylabel('x')

plt.figure(3)
plt.plot(eigen3,x,'b') #will be blue
plt.title('P4.2.c.iii')
plt.legend(['n=3'])
plt.ylabel('x')

# P4.2.d
#--------------------------------------------------------------------------
test1=sps.jn_zeros(0,3)
# these vaues are equal to (2 w Sqrt[L/g])
# we want to find w
wtest=test1/(2*np.sqrt(L/g))
print(f'the actual first three values are {wtest}')

#%% P3.3  See Notes Again
#%% P4.4.a
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps
# first, we again we create a cell-edge grid from -5 to positive 5
# I want to have about 200 cells in my grid, so N=201
bottom=-5
top=5
N=201
ex,h=np.linspace(bottom,top,N,retstep=True)

# We next need our vectors, A and B.
A=np.zeros((N,N))
for n in range(1,N-1,1):
    A[n,n-1]=-1/(2*(h**2))
    A[n,n]=(1/(h**2))+((ex[n]**2)/2)
    A[n,n+1]=-1/(2*(h**2))
    
#Then we set the boundary conditions
# first, if y(0)=
A[0,0]=1
A[N-1,N-1]=-1 #bottom right corner, point (200,200)


#and create the B matrix
B=np.identity(N)
B[0,0]=0
B[N-1,N-1]=0

#and find the eigen-vectors and values
vals,vecs=la.eig(A,B)

# We need the real eps
epsilon=np.real(vals)

# and to sort the eigenvalues and eigenvectors
ind=np.argsort(epsilon)
epsilon=epsilon[ind]
vecs=vecs[:,ind]

# We want to plot the first four states 

# we plot the first few modes, correctly Normalized
eigen1=np.abs(vecs[0:N,0])**2
eigen2=np.abs(vecs[0:N,1])**2
eigen3=np.abs(vecs[0:N,2])**2
eigen4=np.abs(vecs[0:N,3])**2

norm1=np.sum(h*eigen1) #we need the normalization factor
norm2=np.sum(h*eigen2)
norm3=np.sum(h*eigen3)
norm4=np.sum(h*eigen4)

# And re-calculate the eigen-states
eigen1=(1/norm1)*eigen1
eigen2=(1/norm2)*eigen2
eigen3=(1/norm3)*eigen3
eigen4=(1/norm4)*eigen4

#ground state
plt.figure(4)
plt.plot(ex,eigen1,'b') #will be blue
plt.title('P4.4.a.i')
plt.legend(['n=0'])
plt.xlabel('ex')

#excited state 1
plt.figure(5)
plt.plot(ex,eigen2,'b') #will be blue
plt.title('P4.4.a.ii')
plt.legend(['n=1'])
plt.xlabel('ex')

#excited state 2
plt.figure(6)
plt.plot(ex,eigen3,'b') #will be blue
plt.title('P4.4.a.iii')
plt.legend(['n=2'])
plt.xlabel('ex')

#excited state 3
plt.figure(7)
plt.plot(ex,eigen4,'b') #will be blue
plt.title('P4.4.a.iv')
plt.legend(['n=3'])
plt.xlabel('ex')
# P4.4.b---------------------------------------------------------------------
# the epsilon values are apx 0.5, 1.5, 2.5, etc.
print(f'the first five epsilon values are {epsilon[0:5]}')

#%% P4.5--The same as part 4, but we use a different potential function
# first, some boilerplate
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as la
import scipy.special as sps
# first, we again we create a cell-edge grid from -5 to positive 5
# I want to have about 200 cells in my grid, so N=201
bottom=-5
top=5
N=201
ex,h=np.linspace(bottom,top,N,retstep=True)

# We next need our vectors, A and B.
A=np.zeros((N,N))
for n in range(1,N-1,1):
    A[n,n-1]=-1/(2*(h**2))
    #THIS PART IS DIFFERENT---------------------------------------
    A[n,n]=(1/(h**2))+((ex[n]**4)) 
    #THIS PART IS DIFFERENT---------------------------------------
    A[n,n+1]=-1/(2*(h**2))
    
#Then we set the boundary conditions
A[0,0]=1
A[N-1,N-1]=1 #bottom right corner, point (200,200)

#and create the B matrix
B=np.identity(N)
B[0,0]=0
B[N-1,N-1]=0

#and find the eigen-vectors and values
vals,vecs=la.eig(A,B)

# We need the real eps
epsilon=np.real(vals)

# and to sort the eigenvalues and eigenvectors
ind=np.argsort(epsilon)
epsilon=epsilon[ind]
vecs=vecs[:,ind]

# We want to plot the first four states 

# we plot the first few modes, correctly Normalized
eigen1=np.abs(vecs[0:N,0])**2
eigen2=np.abs(vecs[0:N,1])**2
eigen3=np.abs(vecs[0:N,2])**2
eigen4=np.abs(vecs[0:N,3])**2

norm1=np.sum(h*eigen1) #we need the normalization factor
norm2=np.sum(h*eigen2)
norm3=np.sum(h*eigen3)
norm4=np.sum(h*eigen4)

# And re-calculate the eigen-states
eigen1=(1/norm1)*eigen1
eigen2=(1/norm2)*eigen2
eigen3=(1/norm3)*eigen3
eigen4=(1/norm4)*eigen4

#ground state
plt.figure(8)
plt.plot(ex,eigen1,'b') #will be blue
plt.title('P4.5.i')
plt.legend(['n=0'])
plt.xlabel('ex')

#excited state 1
plt.figure(9)
plt.plot(ex,eigen2,'b') #will be blue
plt.title('P4.5.ii')
plt.legend(['n=1'])
plt.xlabel('ex')

#excited state 2
plt.figure(10)
plt.plot(ex,eigen3,'b') #will be blue
plt.title('P4.5.iii')
plt.legend(['n=2'])
plt.xlabel('ex')

#excited state 3
plt.figure(11)
plt.plot(ex,eigen4,'b') #will be blue
plt.title('P4.5.iv')
plt.legend(['n=3'])
plt.xlabel('ex')
# And we print of the first five epsilon values
# the epsilon values are apx 0.5, 1.5, 2.5, etc.
print(f'the first five epsilon values are {epsilon[0:5]}')














