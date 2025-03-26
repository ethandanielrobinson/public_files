# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:29:52 2024

@author: ethan
"""

#%% CSV reading test
import csv
import numpy as np
# Plotting Boilerplate, Credit: Ethan D Robinson
import matplotlib.pyplot as plt
###############################################################################
# We first define the visual style of our plots
###############################################################################
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
###############################################################################
import os # Allows us to change directories
# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script's directory
os.chdir(script_dir)
import FunctionStorage as fst

#-----------------------------------------------------------------------------
# SETTING UP THE RAW DATA
#-----------------------------------------------------------------------------

#we want to be able to define our own endpoint
question=input("How long would you like the x-axis to be? ")
xmax=float(question)

# Now we need to open the data file list
data_path = os.path.join(script_dir, "ASY Files", "3_Long_Field_B", "1_13_Mar_2023")
os.chdir(data_path)

#--------------------------------------------------------------------------
# We create error plots for both the 2K and 3K runs.
output2K=fst.asyopen('2K.asy',xmax)
time2K=output2K[0]
asym2K=output2K[1]
error2K=output2K[2]

output3K=fst.asyopen('3K.asy',xmax)
time3K=output3K[0]
asym3K=output3K[1]
error3K=output3K[2]

# Creating the fits
musr_path = os.path.join(script_dir, "MuSR data", "Fits", "6_LF_A", "1_13_Mar_2024")
os.chdir(musr_path)
fitfile=open("fits.csv")

fitreader=csv.reader(fitfile)

fithead1 = []
fithead1 = next(fitreader)
print(fithead1)

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
dfit=np.zeros(fittotal) # d fit column 6
derror=np.zeros(fittotal) # d error column 7
lamfit=np.zeros(fittotal) #lambda value column 8
lamerror=np.zeros(fittotal) # lambda error column 9

n=0;

# And assign the correct values
while n<fittotal:
    tempfit[n] = float(fitrows[n][0])
    temperror[n] = float(fitrows[n][1])
    afit[n] = float(fitrows[n][2])
    aerror[n] = float(fitrows[n][3])
    betafit[n] = float(fitrows[n][4])
    betaerror[n] = float(fitrows[n][5])
    dfit[n] = float(fitrows[n][6])
    derror[n] = float(fitrows[n][7])
    lamfit[n] = float(fitrows[n][8])
    lamerror[n] = float(fitrows[n][9])
    n = n+1

# we also create plots based on the fitting data
t=np.linspace(0,xmax,500)
T2=fst.highexp(afit[0], betafit[0], lamfit[0], dfit[0], t)
T3=fst.highexp(afit[1], betafit[1], lamfit[1], dfit[1], t)
T4=fst.highexp(afit[2], betafit[2], lamfit[2], dfit[2], t)
T5=fst.highexp(afit[3], betafit[3], lamfit[3], dfit[3], t)
T6=fst.highexp(afit[4], betafit[4], lamfit[4], dfit[4], t)



image_path = os.path.join(script_dir, "images")
os.chdir(image_path)

# And Plot our figure
plt.figure(1)
# T=2K
plt.plot(time2K, asym2K, '#8080FF', marker=".", linestyle='')
plt.errorbar(time2K, asym2K,
             yerr = error2K, 
             fmt = ' ',
             capsize=(4),
             ecolor=('#8080FF'))
plt.plot(t,T2,"#0000FF")
# T=3K
plt.plot(time3K, asym3K, '#80FF80', marker=".", linestyle='')
plt.errorbar(time3K, asym3K,
             yerr = error3K, 
             fmt = ' ',
             capsize=(4),
             ecolor=('#80FF80'))
plt.plot(t,T3,"#00FF00")
plt.xlabel('Time (µs)')
plt.ylabel('A(t)')
plt.ylim([0,0.25])
plt.xlim([0,1])
plt.title("Longitudinal Field With Error Bars")
plt.savefig('LF_demonstration_c', dpi=300)

#%% Other Plots
plt.figure(2)
plt.plot(t,T2,"#123456")
plt.plot(t,T3,"#234561")
plt.plot(t,T4, '#345612')
plt.plot(t,T5, '#456123')
plt.plot(t,T6, '#561234')
plt.xlabel('Time (µs)')
plt.ylabel('A(t)')
plt.ylim([0,0.25])
plt.xlim([0,1])
plt.title("Examples of Longitudinal Curves")
plt.savefig('LF_demonstration_d', dpi=300)