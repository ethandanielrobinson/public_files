# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:15:12 2024

@author: ethan
"""

# Plotting Functions
#Function List
import numpy as np
import csv

# Dampened Cosine Function
def dampcos(a,v,phi,b,t):
    p=np.pi
    A=a*np.cos(2*p*v*t+(p*phi/180))*np.exp(-b*t)
    return A
#Advanced Damped Cosine
def adampcos(a,v,phi,b,d,l,t):
    p=np.pi
    A=a*np.cos(2*p*v*t+(p*phi/180))*np.exp(-b*t)+d*np.exp(-l*t)
    return A

def lowexp(d,l,t):
    A=d*np.exp(-l*t)
    return A

# Streched Exponential Function
def strexp(a,b,l,t):
    A=a*np.exp(-(l*t)**b)
    return A

# Non-zero Exponential
def highexp(a,b,l,d,t):
    A=a*np.exp(-(l*t)**b)+d
    return A

#Numerical Derivitive Function------------------------------------------------
def devone(y,x):
    len1=len(y)
    len2=len(x)
    dx=np.zeros_like(y)
    if len1==len2:
        dx[1:len1-1]=(y[2:]-y[0:13])/(x[2:]-x[0:13])
        # and a quadratic aproximation for the edges
        h1=np.abs(x[1]-y[0])
        h2=np.abs(x[2]-y[0])
        h3=np.abs(x[-1]-y[-2])
        h4=np.abs(x[-1]-y[-3])
        dx[0]=(1/(2*h2))*(x[2])-(2/h1)*(x[1])+(3/(2*h2))*x[0]
        dx[-1]=(1/(2*h4))*(x[-3])-(2/h3)*(x[-2])+(3/(2*h4))*x[-1]
        return dx
    else:
        return 0
    
#CSV Ripping Function---------------------------------------------------------
def asyopen(loc: str, ind: int)->list:
    file1=open(loc) # Open the File
    
    csvreader1 = csv.reader(file1) # Read the file
    
    # Read of the file heading
    header11 = []
    header11 = next(csvreader1)
    header21 = []
    header21 = next(csvreader1)
    header31 = []
    header31 = next(csvreader1)
    
    #Print off the results
    print(header11)
    print(header21)
    print(header31)

    rows1 = []
    for row in csvreader1:
        rows1.append(row)
    file1.close()
    
    
    #find the index for t=ind
    m=0;
    con=0;
    while con==0:
        edr1 = float(rows1[m][0])
        if edr1<=ind:
            m=m+1
        if edr1>ind:
            con=1
    
    total = m
    time=np.zeros(total)
    asym=np.zeros(total)
    error=np.zeros(total)
    
    # initialize our counter
    n=0
       
    # and read in the numbers
    while n<total:
        time[n] = float(rows1[n][0])
        asym[n] = float(rows1[n][1])
        error[n] = float(rows1[n][2])
        n = n+1
    
    output=[time, asym, error]
    return output
