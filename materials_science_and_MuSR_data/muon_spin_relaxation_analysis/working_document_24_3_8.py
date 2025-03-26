# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 22:46:50 2024

@author: ethan
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 09:43:45 2024

@author: ethan
"""
#%% CSV reading test
import csv
import numpy as np
# Plotting Boilerplate, Credit: Ethan D Robinson
from matplotlib import cm
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
# Now we need to open the data file list
data_path = os.path.join(script_dir, "ASY Files", "zero_field_asy", "ns_150")
os.chdir(data_path)

#-----------------------------------------------------------------------------
#T=3.5K
#-----------------------------------------------------------------------------
filea=open('ZF_3d5K.asy')
type(filea)

csvreadera=csv.reader(filea)

header1a = []
header1a = next(csvreadera)
header2a = []
header2a = next(csvreadera)
header3a = []
header3a = next(csvreadera)

rowsa = []
for row in csvreadera:
    rowsa.append(row)
rowsa
filea.close()

# We now create arrays for time, asym, and error
totala=len(rowsa)
timea=np.zeros(totala)
asyma=np.zeros(totala)
errora=np.zeros(totala)

# and set our counter
n=0

while n<totala:
    timea[n] = float(rowsa[n][0])
    asyma[n] = float(rowsa[n][1])
    errora[n] = float(rowsa[n][2])
    n = n+1
#-----------------------------------------------------------------------------
#T=9K
#-----------------------------------------------------------------------------

fileb=open('ZF_9K.asy')
type(fileb)

csvreaderb=csv.reader(fileb)

header1b = []
header1b = next(csvreaderb)
header2b = []
header2b = next(csvreaderb)
header3b = []
header3b = next(csvreaderb)

rowsb = []
for row in csvreaderb:
    rowsb.append(row)
rowsb
fileb.close()

# We now create arrays for time, asym, and error
totalb=len(rowsb)
timeb=np.zeros(totalb)
asymb=np.zeros(totalb)
errorb=np.zeros(totalb)

# and set our counter
n=0

while n<totalb:
    timeb[n] = float(rowsb[n][0])
    asymb[n] = float(rowsb[n][1])
    errorb[n] = float(rowsb[n][2])
    n = n+1
#-----------------------------------------------------------------------------
#T=18K
#-----------------------------------------------------------------------------
filec=open('ZF_18K.asy')
type(filec)

csvreaderc=csv.reader(filec)

header1c = []
header1c = next(csvreaderc)
header2c = []
header2c = next(csvreaderc)
header3c = []
header3c = next(csvreaderc)

rowsc = []
for row in csvreaderc:
    rowsc.append(row)
rowsc
filec.close()

# We now create arrays for time, asym, and error
totalc=len(rowsc)
timec=np.zeros(totalc)
asymc=np.zeros(totalc)
errorc=np.zeros(totalc)

# and set our counter
n=0

while n<totalc:
    timec[n] = float(rowsc[n][0])
    asymc[n] = float(rowsc[n][1])
    errorc[n] = float(rowsc[n][2])
    n = n+1


#%%
#-----------------------------------------------------------------------------
#Importing Fitting Data
#-----------------------------------------------------------------------------
musr_path = os.path.join(script_dir, "MuSR data", "Fits", "ZF_A", "ns_150")
os.chdir(musr_path) 
fitfile=open("zero_field_params.csv")

fitreader=csv.reader(fitfile)

fithead1 = []
fithead1 = next(fitreader)

fitrows=[]
for row in fitreader:
    fitrows.append(row)
fitrows
fitfile.close()

#intialize our catagores
fittotal=len(fitrows)
tempfit=np.zeros(fittotal) #temperatures column 0
temperror=np.zeros(fittotal) # temp error, column 1
afit=np.zeros(fittotal) #a value column 2
aerror=np.zeros(fittotal) # a error column 3
betafit=np.zeros(fittotal) #beta values column 4
betaerror=np.zeros(fittotal) # beta error column 5
lamfit=np.zeros(fittotal) #lambda value column 6
lamerror=np.zeros(fittotal) # lambda error column 7

n=0;

# And assign the correct values
while n<fittotal:
    tempfit[n] = float(fitrows[n][0])
    temperror[n] = float(fitrows[n][1])
    afit[n] = float(fitrows[n][2])
    aerror[n] = float(fitrows[n][3])
    betafit[n] = float(fitrows[n][4])
    betaerror[n] = float(fitrows[n][5])
    lamfit[n] = float(fitrows[n][6])
    lamerror[n] = float(fitrows[n][7])
    n = n+1

# Define our timescale
N=500;
xlength=10;

# Define t from 0 to 10 microseconds
t=np.linspace(0,xlength,N)

#-----------------------------------------------------------------------------
# SETTING UP THE FIT FOR 3.5K
#-----------------------------------------------------------------------------
# new fits
fitsa=fst.strexp(afit[1], betafit[1], lamfit[1], t)
#-----------------------------------------------------------------------------
# SETTING UP THE FIT FOR 9K
#-----------------------------------------------------------------------------
fitsb=fst.strexp(afit[4], betafit[4], lamfit[4], t)
#-----------------------------------------------------------------------------
# SETTING UP THE FIT FOR 18K
#-----------------------------------------------------------------------------
fitsc=fst.strexp(afit[10], betafit[10], lamfit[10], t)
#%%
image_path = os.path.join(script_dir, "images")
os.chdir(image_path)

# And Now We Plot
plt.figure(1)
# For 3.5 K
plt.plot(timea, asyma, '#8080FF', marker=".", linestyle='')
plt.errorbar(timea,asyma,
             yerr = errora, 
             fmt = ' ',
             capsize=(4),
             ecolor=('#8080FF'))
plt.plot(t,fitsa,'#0000FF')
# For 9 K
plt.plot(timeb, asymb, '#FF8080', marker=".", linestyle='')
plt.errorbar(timeb,asymb,
             yerr = errorb, 
             fmt = ' ',
             capsize=(4),
             ecolor=('#FF8080'))
plt.plot(t,fitsb,'#FF0000')
# For 18 K
plt.plot(timec, asymc, '#80FF80', marker=".", linestyle='')
plt.errorbar(timec,asymc,
             yerr = errorc, 
             fmt = ' ',
             capsize=(4),
             ecolor=('#80FF80'))
plt.plot(t,fitsc,'#00FF00')
plt.legend(('3.5K Actual','3.5K Plotted','9K Actual','9K Plotted','18K Actual','18K Plotted'),ncol=3)
plt.xlabel('Time (µs)')
plt.ylabel('A(t)')
plt.ylim([0,0.25])
plt.xlim([0,10])
plt.savefig('multiple_plots_ZF', dpi=300)

#%%
# Plot the full fits

# Define the color map from dark blue to red
colors = cm.copper(np.linspace(0, 1, 18))

plt.figure(2)
j=0;
fitd=np.zeros_like(t)

while j<fittotal:
    fitd=fst.strexp(afit[j], betafit[j], lamfit[j], t)
    plt.plot(t,fitd,color=colors[j])
    j=j+1
plt.xlabel('Time (µs)')
plt.ylabel('A(t)')
plt.ylim([0,0.25])
plt.xlim([0,10])
plt.savefig('all_plots_ZF', dpi=300)

#%% Uncertainty plots    
image_path = os.path.join(script_dir, "images")
os.chdir(image_path)

plt.figure(3)
plt.plot(tempfit,lamerror,'#000000')
plt.xlabel('Temperature (K)')
plt.ylabel('ε(λ)')
plt.yscale('log') # give the y-axis a log scale
plt.ylim([0.001,100000])
plt.xlim([0,60])
plt.savefig('lam_error', dpi=300)

#%% Building a better plot for the numerical integration in 150ns
os.chdir('D:\\Research\\Reports')

filen=open("ZF_150ns.csv")
type(filen)

csvreadern=csv.reader(filen)

header1n = []
header1n = next(csvreadern)
header2n = []
header2n = next(csvreadern)
header3n = []
header3n = next(csvreadern)

rowsn = []
for row in csvreadern:
    rowsn.append(row)
rowsn
filen.close()

# We now create arrays for time, asym, and error
totaln = len(rowsn)
tempn = np.zeros(totaln)
intasyn = np.zeros(totaln)
errorn = np.zeros(totaln)

# and set our counter
n=0

while n<totaln:
    tempn[n] = float(rowsn[n][0])
    intasyn[n] = float(rowsn[n][1])
    errorn[n] = float(rowsn[n][2])
    n = n+1

os.chdir('D:\Research\Images\images_24_2_26')

#And Now We Plot
plt.plot(4)
plt.figure().set_figwidth(5)
plt.plot(tempn, intasyn, 'o', markerfacecolor='none', markeredgecolor='#000000', markersize=8)
plt.errorbar(tempn,intasyn,
             yerr = errorn, 
             fmt = ' ',
             capsize=(8),
             ecolor=('#808080'))
plt.xlim([0,60])
plt.ylim([-0.1,1])
plt.xlabel('Temperature (K)')
plt.ylabel('∫A(t) dt')
plt.savefig('int_150_ZF', dpi=300)

#%% Building a better plot for the numerical integration in 5ns
os.chdir('D:\\Research\\Reports')

filem=open("ZF_5ns_temp.csv")
type(filem)

csvreaderm=csv.reader(filem)

header1m = []
header1m = next(csvreaderm)
header2m = []
header2m = next(csvreaderm)
header3m = []
header3m = next(csvreaderm)

rowsm = []
for row in csvreaderm:
    rowsm.append(row)
rowsm
filem.close()

# We now create arrays for time, asym, and error
totalm = len(rowsm)
tempm = np.zeros(totalm)
intasym = np.zeros(totalm)
errorm = np.zeros(totalm)

# and set our counter
n=0

while n<totaln:
    tempm[n] = float(rowsm[n][0])
    intasym[n] = float(rowsm[n][1])
    errorm[n] = float(rowsm[n][2])
    n = n+1

os.chdir('D:\Research\Images\images_24_2_26')

#And Now We Plot
plt.plot(5)
plt.figure().set_figwidth(5)
plt.plot(tempm, intasym, 'o', markerfacecolor='none', markeredgecolor='#000000', markersize=8)
plt.errorbar(tempm,intasym,
             yerr = errorm, 
             fmt = ' ',
             capsize=(8),
             ecolor=('#808080'))
plt.xlim([0,60])
plt.ylim([-0.01,0.12])
plt.xlabel('Temperature (K)')
plt.ylabel('∫A(t) dt')
plt.savefig('int_5_temp', dpi=300)
#%%
# And change the directory back
os.chdir('D:\Research\Reports\python')



#%% TEST AREA
print(afit[10], betafit[10], lamfit[10])