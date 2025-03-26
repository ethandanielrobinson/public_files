# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 12:12:29 2024

@author: ethan
"""

# Ethan D Robinson
# BYU Department of Physics and Astronomy
# Working notes, 9 March 2024

# I opted to direclty plot the fitting parameteters here rather than grabing them
# from the csv file.
#%% LF Transition Plots
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

# Define our timescale
N=500;
xlength=10;

# Define t from 0 to 10 microseconds
t=np.linspace(0,xlength,N)

# We then define the various values
# I previously did this in mathmatica, so the values can't be dirctly reported
# So, I'll probably want to redo this at some point in the future.

tempfits = np.array([2, 3, 4, 5, 5.867, 7, 7.926, 8.8, 9.659, 11.787, 13.494, 
                     15.283, 17.556, 19.42, 21.304, 24.653, 29.946, 
                     40.32, 50.7, 60, 70])

temperror = np.array([0, 0, 0, 0, 0.007, 0, 0.006, 0, 0.006, 0.007, 0.006, 
                      0.011, 0.004, 0.003, 0.002, 0.006, 0.024, 0.07, 0.23, 
                      0, 0])

betafits = np.array([0.08916, 0.10045, 0.14033, 0.15902, 0.16387, 0.21942, 
                     0.34179, 0.40316, 0.45861, 0.50443, 0.53581, 0.53945, 
                     0.54730, 0.55753, 0.56323, 0.56910, 0.60473, 0.63085, 
                     0.71079, 0.74233, 0.77299])

lamfits = np.array([27.57793, 42.46112, 23.09352, 30.68466, 47.92025, 
                    17.55965, 5.58306, 2.79641, 1.82278, 0.86216, 
                    0.58404, 0.45182, 0.35527, 0.31429, 0.28116, 0.23978, 
                    0.21156, 0.16573, 0.15875, 0.13828, 0.12244])

image_path = os.path.join(script_dir, "images")
os.chdir(image_path)

fittotal=len(tempfits)

#The a values are all 0.25
afits=0.25*np.ones_like(betafits)

# Define the color map from dark blue to red
colors = cm.copper(np.linspace(0, 1, 21))

plt.figure(2)
j=0;
fitd=np.zeros_like(t)

while j<fittotal:
    fitd=fst.strexp(afits[j], betafits[j], lamfits[j], t)
    plt.plot(t,fitd,color=colors[j])
    j=j+1
plt.xlabel('Time (µs)')
plt.ylabel('A(t)')
plt.title('LF=4000G, All Plots')
plt.ylim([0,0.25])
plt.xlim([0,10])
plt.savefig('all_plots_LF', dpi=300)








