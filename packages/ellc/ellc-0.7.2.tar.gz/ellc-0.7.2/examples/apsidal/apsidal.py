#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function,
                            unicode_literals)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--eps", help="genereate .eps file", action="store_true")
args = parser.parse_args()

if args.eps:
  import matplotlib
  matplotlib.use('Agg')

import numpy as np
import ellc
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline

# Load downloaded data from the paper
table = np.load('minima_dat.npy') 
# Extract data for the star of interest
star ='OGLE-SMC-ECL-0720'
tmin_obs = (table['HJD'])[table['Name'] == star]
tmin_err = (table['e_HJD'])[table['Name'] == star]
tmin_type = (table['Type'])[table['Name'] == star]

# Parameters from the paper
T_0    = 53803.390 
p_siderial = 6.052322  
ecc = 0.062
omdot =  0.2070
period = p_siderial/(1-omdot/360)   # Anomalistic period
omega_0 = 67.6
f_c = np.sqrt(ecc)*np.cos(omega_0*np.pi/180.)
f_s = np.sqrt(ecc)*np.sin(omega_0*np.pi/180.)
incl = 84.57
t_step = 0.001
# Calculate t_zero from for T_0 
# (T_0 is halfway between a time of primary and secondary eclipse) 
time_calc1,lc1 = ellc.tmin([T_0+0.5*p_siderial], t_step, T_0, period,
 f_c=f_c, f_s=f_s, omdot=omdot, incl=incl, n_grid=801)
t_zero = T_0 - (time_calc1[0] - (T_0+0.5*p_siderial))/2

# Now predict times of eclipse
tmin_calc,lc = ellc.tmin(tmin_obs, t_step, t_zero, period,
 f_c=f_c, f_s=f_s, omdot=omdot, incl=incl, n_grid=101)

# Print results to screen
fmt = '{0:.4f} {1:.4f} {2:.4f} {3:8.4f} {4:2s}'
res = tmin_obs-tmin_calc
for i in range(0,len(tmin_calc)):
 print(fmt.format(tmin_obs[i], tmin_err[i],tmin_calc[i] ,res[i], tmin_type[i]))

# Create a plot
t_pri = tmin_obs[tmin_type =='Prim']
e_pri = tmin_err[tmin_type =='Prim']
c_pri = np.rint((t_pri-t_zero)/p_siderial)
t_sec = tmin_obs[tmin_type =='Sec']
e_sec = tmin_err[tmin_type =='Sec']
c_sec = np.rint((t_sec-t_zero -0.5*p_siderial)/p_siderial) + 0.5
y_pri = t_pri - (t_zero+p_siderial*c_pri)
y_sec = t_sec - (t_zero+p_siderial*c_sec)
fig=plt.figure(star, figsize=(6,3))
plt.errorbar(c_pri,y_pri,yerr=e_pri,color='darkblue',fmt='o')
plt.errorbar(c_sec,y_sec,yerr=e_sec,color='darkgreen',fmt='o')
cgrid = np.arange(np.min([c_pri,c_sec])-10,np.max([c_pri,c_sec])+10)
tfit_pri = tmin_calc[tmin_type =='Prim']
tfit_sec = tmin_calc[tmin_type =='Sec']
c_grid = np.arange(np.min([c_pri,c_sec])-100,np.max([c_pri,c_sec])+100)
c_pri_uniq,i_pri_uniq = np.unique(c_pri, return_index=True)
spl = InterpolatedUnivariateSpline(c_pri_uniq,tfit_pri[i_pri_uniq])
t_pri_grid = spl(c_grid)
c_sec_uniq,i_sec_uniq = np.unique(c_sec, return_index=True)
spl = InterpolatedUnivariateSpline(c_sec_uniq,tfit_sec[i_sec_uniq])
t_sec_grid = spl(c_grid)
plt.plot(c_grid,t_pri_grid - (t_zero+p_siderial*c_grid),color='darkblue')
plt.plot(c_grid,t_sec_grid - (t_zero+p_siderial*c_grid),color='darkgreen')
plt.xlabel('Cycle')
plt.ylabel('O-C [d]')
plt.xlim([np.min([c_pri,c_sec])-100,np.max([c_pri,c_sec])+100])

plt.tight_layout()

if args.eps:
  fig.savefig("apsidal.eps")
else:
  plt.show()
