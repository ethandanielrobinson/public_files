# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 11:39:13 2024

@author: ethan
"""

#%% CSV reading test
import csv
import numpy as np
# Plotting Boilerplate, Credit: Ethan D Robinson
import matplotlib.pyplot as plt
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['axes.edgecolor'] = '#000000'
plt.rcParams['axes.labelcolor'] = '#000000'
plt.rcParams['axes.labelsize'] = 'large'
#--------------------------------------
plt.rcParams['axes.titlecolor'] = '#000000'
plt.rcParams['axes.titlesize'] = 'large'
plt.rcParams['axes.titleweight'] = 'heavy'
plt.rcParams['figure.facecolor'] = '#FFFFFF'
#--------------------------------------
plt.rcParams['xtick.color'] = '#000000'
plt.rcParams['ytick.color'] = '#000000'

import os # Allows us to change directories
# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script's directory
os.chdir(script_dir)

import FunctionStorage as fst 
#-----------------------------------------------------------------------------
# SETTING UP THE RAW DATA
#-----------------------------------------------------------------------------
data_path = os.path.join(script_dir, "ASY Files", "long_field_asy", "5ns")
os.chdir(data_path)
#-----------------------------------------------------------------------------
#T=4K, B=4000G, Long.
#-----------------------------------------------------------------------------
file1=open('4000G_4K.asy')
type(file1)

csvreader1 = csv.reader(file1)

header11 = []
header11 = next(csvreader1)
header21 = []
header21 = next(csvreader1)
header31 = []
header31 = next(csvreader1)

rows1 = []
for row in csvreader1:
    rows1.append(row)
rows1
file1.close()

# We now create arrays for time, asym, and error
total1=len(rows1)
time1=np.zeros(total1)
asym1=np.zeros(total1)
error1=np.zeros(total1)

# and set our counter
n=0

while n<total1:
    time1[n] = float(rows1[n][0])
    asym1[n] = float(rows1[n][1])
    error1[n] = float(rows1[n][2])
    n = n+1
    
#find the index for t=1
m=0;
con=0;
while con==0:
    edr1=time1[m]
    if edr1<=1:
        m=m+1
    if edr1>1:
        con=1
        
#-----------------------------------------------------------------------------
#Importing Fitting Data
#-----------------------------------------------------------------------------
t=np.linspace(0,1,500) 
T7=fst.highexp(0.25000, 0.80441, 30.32858, 0.05582, t)

#----------------------------------------------------------------------------
# Ensuring that time1 only goes to t=1
#----------------------------------------------------------------------------
timeplot=time1[0:m]
asymplot=asym1[0:m]
errorplot=error1[0:m]

image_path = os.path.join(script_dir, "images")
os.chdir(image_path)

# And Plot our figure
plt.figure(1)
plt.plot(timeplot,asymplot, '#8080FF', marker=".", linestyle='')
plt.errorbar(timeplot,asymplot,
             yerr = errorplot, 
             fmt = ' ',
             capsize=(4),
             ecolor=('#8080FF'))
plt.plot(t,T7,'#0000FF')
plt.xlabel('Time (µs)')
plt.ylabel('A(t)')
plt.title('LF=4000G, T=4K, Δt=5ns')
plt.ylim([0,0.25])
plt.xlim([0,1])
plt.savefig('LF_demonstration', dpi=300)
#%% Test Space
print(type(header31[0]))