# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 00:16:16 2023

@author: ethan
"""

#%% LAB 11
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P11.1
# See Handwritten Notes
#%% P11.2
# See Handwritten Notes
#%% P11.3 & P11.4.a
import Lab11Funcs as S
import matplotlib.pyplot as plt
import numpy as np

# System Parameters
L = 10.0 # Length of tube
T0 = 293. # Ambient temperature
rho0 = 1.3 # static density (sea level)

# speed of sound
c = np.sqrt(S.gamma * S.kB * T0 / S.M)
# cell-center grid with ghost points
N = 100
h = L/N
x = np.linspace(-.5*h,L+.5*h,N+2)

# initial distributions
rho = rho0 * np.ones_like(x)
T = T0 * np.ones_like(x)
v = np.exp(-200*(x/L-0.5)**2) * c/100

tau = 1e-4
tfinal = 0.1
t = np.arange(0,tfinal,tau)

skip = 5 #input(' Steps to skip between plots - ')

for n in range(len(t)):
    # Plot the current values before stepping
    if n % skip == 0:
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(x,rho)
        plt.ylabel('rho')
        plt.ylim(1.28, 1.32)
        plt.title('time={:1.3f}'.format(t[n]))
        plt.subplot(3,1,2)
        plt.plot(x,T)
        plt.ylabel('T')
        plt.ylim(292,294)
        plt.subplot(3,1,3)
        plt.plot(x,v)
        plt.ylabel('v')
        plt.ylim(-4,4)
        plt.xlabel('x')
        plt.pause(0.05)
        
    # 1. Predictor step for rho
    rhop = S.Srho(rho,v,v,tau,h)
    
    # 2. Predictor step for T
    Tp = S.ST(T,v,v,rho,rhop,tau,h)
    
    # 3. Predictor step for v
    vp = S.Sv(v,v,v,rho,rhop,T,Tp,tau,h)
    
    # 4. Corrector step for rho
    rhop = S.Srho(rho,v,vp,tau,h)
    
    # 5. Corrector step for T
    Tp = S.ST(T,v,vp,rho,rhop,tau,h)
    
    # 6. Corrector step for v
    v = S.Sv(v,v,vp,rho,rhop,T,Tp,tau,h)
    
    # Now put rho and T at the same time-level as v
    rho = rhop
    T = Tp
    
#%% P11.4.b
import Lab11Funcs as S
import matplotlib.pyplot as plt
import numpy as np

# System Parameters
L = 10.0 # Length of tube
T0 = 293. # Ambient temperature
rho0 = 1.3 # static density (sea level)

# speed of sound
c = np.sqrt(S.gamma * S.kB * T0 / S.M)
# cell-center grid with ghost points
# We allow the user to define N
nin=input("What value would you like for N? N was 100 in part a: ")
N=int(nin)

h = L/N
x = np.linspace(-.5*h,L+.5*h,N+2)

# initial distributions
rho = rho0 * np.ones_like(x)
T = T0 * np.ones_like(x)
v = np.exp(-200*(x/L-0.5)**2) * c/100

#-------------------------------------------------
# We allow our user to define their own tau values
#-------------------------------------------------
tin=input("What value would you like for tau? Tau was 0.0001 in part a: ")
tau=float(tin)

tfinal = 0.1
t = np.arange(0,tfinal,tau)

skip = 40 #input(' Steps to skip between plots - ')

for n in range(len(t)):
    # Plot the current values before stepping
    if n % skip == 0:
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(x,rho)
        plt.ylabel('rho')
        plt.ylim(1.28, 1.32)
        plt.title('time={:1.3f}'.format(t[n]))
        plt.subplot(3,1,2)
        plt.plot(x,T)
        plt.ylabel('T')
        plt.ylim(292,294)
        plt.subplot(3,1,3)
        plt.plot(x,v)
        plt.ylabel('v')
        plt.ylim(-4,4)
        plt.xlabel('x')
        plt.pause(0.05)
        
    # 1. Predictor step for rho
    rhop = S.Srho(rho,v,v,tau,h)
    
    # 2. Predictor step for T
    Tp = S.ST(T,v,v,rho,rhop,tau,h)
    
    # 3. Predictor step for v
    vp = S.Sv(v,v,v,rho,rhop,T,Tp,tau,h)
    
    # 4. Corrector step for rho
    rhop = S.Srho(rho,v,vp,tau,h)
    
    # 5. Corrector step for T
    Tp = S.ST(T,v,vp,rho,rhop,tau,h)
    
    # 6. Corrector step for v
    v = S.Sv(v,v,vp,rho,rhop,T,Tp,tau,h)
    
    # Now put rho and T at the same time-level as v
    rho = rhop
    T = Tp

# The equation I got for taumax is tau=(0.448/((L/h)-3.394))
#%% P11.3.c
import Lab11Funcs2 as S2
import matplotlib.pyplot as plt
import numpy as np

# System Parameters
L = 10.0 # Length of tube
T0 = 293. # Ambient temperature
rho0 = 1.3 # static density (sea level)

# speed of sound
c = np.sqrt(S2.gamma * S2.kB * T0 / S2.M)
# cell-center grid with ghost points
N = 100
h = L/N
x = np.linspace(-.5*h,L+.5*h,N+2)

# initial distributions
rho = rho0 * np.ones_like(x)
T = T0 * np.ones_like(x)
v = np.exp(-200*(x/L-0.5)**2) * c/10

tau = 1e-4
tfinal = 0.2
t = np.arange(0,tfinal,tau)

skip = 5 #input(' Steps to skip between plots - ')

for n in range(len(t)):
    # Plot the current values before stepping
    if n % skip == 0:
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(x,rho)
        plt.ylabel('rho')
        plt.ylim(1.20, 1.40)
        plt.title('time={:1.3f}'.format(t[n]))
        plt.subplot(3,1,2)
        plt.plot(x,T)
        plt.ylabel('T')
        plt.ylim(286,300)
        plt.subplot(3,1,3)
        plt.plot(x,v)
        plt.ylabel('v')
        plt.ylim(-20,20)
        plt.xlabel('x')
        plt.pause(0.05)
        
    # 1. Predictor step for rho
    rhop = S2.Srho(rho,v,v,tau,h)
    
    # 2. Predictor step for T
    Tp = S2.ST(T,v,v,rho,rhop,tau,h)
    
    # 3. Predictor step for v
    vp = S2.Sv(v,v,v,rho,rhop,T,Tp,tau,h)
    
    # 4. Corrector step for rho
    rhop = S2.Srho(rho,v,vp,tau,h)
    
    # 5. Corrector step for T
    Tp = S2.ST(T,v,vp,rho,rhop,tau,h)
    
    # 6. Corrector step for v
    v = S2.Sv(v,v,vp,rho,rhop,T,Tp,tau,h)
    
    # Now put rho and T at the same time-level as v
    rho = rhop
    T = Tp
    
#%% P11.4.d
import Lab11Funcs as S
import matplotlib.pyplot as plt
import numpy as np

# System Parameters
L = 10.0 # Length of tube
T0 = 293. # Ambient temperature
rho0 = 1.3 # static density (sea level)

# speed of sound
c = np.sqrt(S.gamma * S.kB * T0 / S.M)
# cell-center grid with ghost points
N = 100
h = L/N
x = np.linspace(-.5*h,L+.5*h,N+2)

# initial distributions
rho = rho0 * np.ones_like(x)
T = T0 * np.ones_like(x)
v = np.exp(-200*(x/L-0.5)**2) * c/10 # THIS PART IS DIFFERENT-----------------

tau = 1e-4
tfinal = 0.1
t = np.arange(0,tfinal,tau)

skip = 5 #input(' Steps to skip between plots - ')

for n in range(len(t)):
    # Plot the current values before stepping
    if n % skip == 0:
        plt.clf()
        plt.subplot(3,1,1)
        plt.plot(x,rho)
        plt.ylabel('rho')
        plt.ylim(1.20, 1.40)
        plt.title('time={:1.3f}'.format(t[n]))
        plt.subplot(3,1,2)
        plt.plot(x,T)
        plt.ylabel('T')
        plt.ylim(286,300)
        plt.subplot(3,1,3)
        plt.plot(x,v)
        plt.ylabel('v')
        plt.ylim(-20,20)
        plt.xlabel('x')
        plt.pause(0.05)
        
    # 1. Predictor step for rho
    rhop = S.Srho(rho,v,v,tau,h)
    
    # 2. Predictor step for T
    Tp = S.ST(T,v,v,rho,rhop,tau,h)
    
    # 3. Predictor step for v
    vp = S.Sv(v,v,v,rho,rhop,T,Tp,tau,h)
    
    # 4. Corrector step for rho
    rhop = S.Srho(rho,v,vp,tau,h)
    
    # 5. Corrector step for T
    Tp = S.ST(T,v,vp,rho,rhop,tau,h)
    
    # 6. Corrector step for v
    v = S.Sv(v,v,vp,rho,rhop,T,Tp,tau,h)
    
    # Now put rho and T at the same time-level as v
    rho = rhop
    T = Tp
#%% TEST SPACE
import Lab11Funcs as S
import matplotlib.pyplot as plt
import numpy as np

# System Parameters
L = 10.0 # Length of tube
T0 = 293. # Ambient temperature
rho0 = 1.3 # static density (sea level)

# speed of sound
c = np.sqrt(S.gamma * S.kB * T0 / S.M)
# cell-center grid with ghost points
N = 100
h = L/N
x = np.linspace(-.5*h,L+.5*h,N+2)