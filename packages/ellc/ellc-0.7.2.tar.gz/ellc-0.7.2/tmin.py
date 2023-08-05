# This file is part of the ellc binary star model
# Copyright (C) 2016 Pierre Maxted
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from ellc import ellc_f
from scipy.interpolate import InterpolatedUnivariateSpline

def tmin(tmin_obs, t_step, t_zero, period, n_grid = 21, 
         radius_1=0.1, radius_2=0.1, sbratio=1, incl=90, a = None, q = 1,
       f_c = None, f_s = None, omdot = None, didt = None,
       ld_1=None, ldc_1 = None, ld_2=None, ldc_2 = None,
       gdc_1 = None, gdc_2 = None, rotfac_1 = 1, rotfac_2 = 1,
       bfac_1 = None, bfac_2 = None, heat_1 = None, heat_2 = None, 
       grid_1='default', grid_2='default',
       shape_1='sphere', shape_2='sphere',
       spots_1=None, spots_2=None, verbose=1):
  """
  Calculate the times of minimum light for an eclipsing binary star

  This function calculates the light curve of a binary star using the ellc
  binary star model [1] at times near observed times of minimum light and
  reports the predicted time of minimum light for a given set of model
  parameters.

  Parameters
  ----------
  tmin_obs : array_like
      Measured times of minimum light.

  t_step : float
      Time step for calculated light curves

  t_zero : float
      Reference time of mid-eclipse for star 1 by star 2.
      The units and time system must be consistent with the values in t_obs.

  period : float
      Orbital period of the binary.
      For binary systes with apsidal motion, this is the anomalistic period.
      If light-time effect or Doppler boosting is to be calculated correctly
      then the units of period must be days, otherwise arbitrary units can be
      used provided that these are consistent with t_zero and tmin_obs.

  n_grid : integer
      Number of grid points used to find the time of minimum light.
      Default is 21

  radius_1 : float, optional
      Radius of star 1 in units of the semi-major axis of the binary.
      The radius is defined to be the same as a sphere with the same volume as
      the ellipsoid used to approximate the shape of the star.
      Set radius_1=1 to fix radius at limiting radius in the Roche potential.
      Default is 0.1

  radius_2 : float, optional
      Radius of star 2 in units of the semi-major axis of the binary.
      The radius is defined to be the same as a sphere with the same volume as
      the ellipsoid used to approximate the shape of the star.
      Set radius_2=1 to fix radius at limiting radius in the Roche potential.
      Default is 0.1

  sbratio : float, optional
      Surface brightness ratio, S_2/S_1 
      Default is 1

  incl : float, optional
      Inclination in degrees.
      Default is 90

  a : {None, float}, optional
      Semi-major axis in solar radii for calculation of light travel time
      and Doppler boosting.

  q : float, optional
      Mass ratio m_2/m_1.
      Default is 1.

  f_c : {None, float},  optional
      For eccentric orbits with eccentricity e and longitude of periastron
      omega_0 and time t_zero,
      f_c = sqrt(e).cos(omega_0)
      If not None, then f_s must also be specified.
      Default is None.

  f_s : {None, float},  optional
      For eccentric orbits with eccentricity e and longitude of periastron 
      omega_0 and time t_zero,
      f_s = sqrt(e).sin(omega_0)
      If not None, then f_c must also be specified.
      Default is None.

  omdot : {None, float},  optional
      Apsidal motion rate  [degrees/siderial period].
      Default is None.

  didt : {None, float},  optional
      Rate of change of inclination [degrees/anomalistic period]
      Default is None.

  ld_1 : {None, "lin", "quad", "sing", "claret", "log", "sqrt", "exp"} 
   Limb darkening law for star 1
   Default is None

  ldc_1 : {None, float, 2-, 3- or 4-tuple of floats}, optional
      Limb darkening coefficients for star 1.
      Number of elements must match the selected limb-darkening law.
      Default is None

  ld_2 : {None, "lin", "quad", "sing", "claret", "log", "sqrt", "exp"} 
   Limb darkening law for star 2
   Default is None

  ldc_2 : {None, float, 2-, 3- or 4-tuple of floats}, optional
      Limb darkening coefficients for star 2.
      Number of elements must match the selected limb-darkening law.
      Default is None

  gdc_1 : {None, float},  optional
      Gravity darkening exponent for star 1.

  gdc_2 : {None, float},  optional
      Gravity darkening exponent for star 2.

  rotfac_1 : float, optional
      Asynchronous rotation factor for star 1, F_1
      Default is 1.

  rotfac_2 : float, optional
      Asynchronous rotation factor for star 2, F_2
      Default is 1.

  bfac_1 : {None, float}, optional
      Doppler boosting factor, star 1
      N.B. Doppler boosting is not calculated is parameter a is None
      Default is None.
      
  bfac_2 : {None, float}, optional
      Doppler boosting factor, star 2
      N.B. Doppler boosting is not calculated is parameter a is None
      Default is None.

  heat_1 : {None, scalar, 3-tuple of floats}, optional
      If scalar, coefficient of simplified reflection model.
      If 3-tuple, parameters of heating+reflection model for star 1, [H_0, H_1, u_H]
      H_0 is the coefficient, H_1 is the exponent and u_H is the linear
      limb-darkening coefficient.
      Default is None.
  
  heat_2 : {None, scalar, 3-tuple of floats}, optional
      If scalar, coefficient of simplified reflection model.
      If 3-tuple, parameters of heating+reflection model for star 1, [H_0, H_1, u_H]
      H_0 is the coefficient, H_1 is the exponent and u_H is the linear
      limb-darkening coefficient.
      Default is None.
  
      
  grid_1 : {"very_sparse", "sparse", "default", "fine", "very_fine"}, optional
      Grid size used to calculate the flux from star 1.
      Default is "default"

  grid_2 : {"very_sparse", "sparse", "default", "fine", "very_fine"}, optional
      Grid size used to calculate the flux from star 2.
      Default is "default"

  shape_1 : {"roche", "sphere", "poly1p5", "poly3p0"}
      Model used to calculate the shape of star 1 - see Notes. 
      Default is "sphere".

  shape_2 : {"roche", "sphere", "poly1p5", "poly3p0"}
      Model used to calculate the shape of star 2 - see Notes. 
      Default is "sphere".

  spots_1 : (4, n_spots_1) array_like
   Parameters of the spots on star 1. For each spot the parameters, in order,
   are latitude, longitude, size and brightness factor. All three angles are
   in degrees.

  spots_2 : (4, n_spots_2) array_like
   Parameters of the spots on star 2. For each spot the parameters, in order,
   are latitude, longitude, size and brightness factor. All three angles are
   in degrees.

  Returns
  -------
  tmin_calc, lc : (n_obs) ndarray, (2, n_obs, n_grid) ndarray
      tmin_calc contains n_obs calculated times of minimum light
      lc[0,i_obs,:] is the grid of times for model fluxes lc[1,i_obs,:] used 
      to calculate the time of minimum light near tmin_obs[i_obs]

  Notes
  -----

     The time of minimum light is calculated from spline fit to the light curve
    calculated over n_grid points centred at the observed time of minimum
    light on a uniform grid of times with grid-spacing t_step.

     Where the light curve do not have a minimum within the range calculated
     the value of tmin_calc will be set to NaN.

     See function lc() in this module for definitions of the parameters used to
    calculate the light curves. 

  Examples
  --------
  A very simple test case.

    >>> import numpy as np
    >>> from tmin import tmin
    >>> period = 2.0
    >>> t_zero = 5000.0
    >>> t_err = 0.002
    >>> c = [-1,3,6,9]
    >>> tmin_obs = t_zero + np.array(c)*period + np.random.normal(0,t_err,4)
    >>> tmin_calc,lc = ellc.tmin(tmin_obs,0.001,t_zero,period)
    >>> for i in range(0,len(tmin_obs)):
    ...  print '{0:3d} {1:.3f} {2:.3f}'.format(c[i], tmin_obs[i], tmin_calc[i])
    ... 
     -1 4998.003 4998.000
      3 5006.002 5006.000
      6 5011.994 5012.000
      9 5018.001 5018.000

  Times of eclipse with apsidal motion for the eclipsing binary
  OGLE-SMC-ECL-0720  from Zasche et al. (2014A&A...572A..71Z)

    >>> import numpy as np
    >>> import ellc
    >>> import matplotlib.pyplot as plt
    >>> from scipy.interpolate import InterpolatedUnivariateSpline
    >>> from ftplib import FTP
    >>> 
    >>> # Download data from the paper via ftp
    >>> data = []
    >>> def append_data(more_data):
    >>>      data.append(more_data)
    >>> 
    >>> ftp =  FTP('cdsarc.u-strasbg.fr')
    >>> ftp.login()
    >>> ftp.retrlines("RETR pub/cats/J/A+A/572/A71/minima.dat",callback=append_data)
    >>> ftp.close()
    >>> # Convert text to a structured array
    >>> table = np.loadtxt(data,usecols=[0,1,2,3],
    >>>   dtype={'names': ('Name','HJD','e_HJD','Type'),
    >>>          'formats': ('S17','f8','f8','S4')})
    >>> # Extract data for the star of interest
    >>> star ='OGLE-SMC-ECL-0720'
    >>> tmin_obs = (table['HJD'])[table['Name'] == star]
    >>> tmin_err = (table['e_HJD'])[table['Name'] == star]
    >>> tmin_type = (table['Type'])[table['Name'] == star]
    >>> 
    >>> # Parameters from the paper
    >>> T_0    = 53803.390 
    >>> p_siderial = 6.052322  
    >>> ecc = 0.062
    >>> omdot =  0.2070
    >>> period = p_siderial/(1-omdot/360)   # Anomalistic period
    >>> omega_0 = 67.6
    >>> f_c = np.sqrt(ecc)*np.cos(omega_0*np.pi/180.)
    >>> f_s = np.sqrt(ecc)*np.sin(omega_0*np.pi/180.)
    >>> incl = 84.57
    >>> t_step = 0.001
    >>> # Calculate t_zero from for T_0 
    >>> # (T_0 is halfway between a time of primary and secondary eclipse) 
    >>> time_calc1,lc1 = ellc.tmin([T_0+0.5*p_siderial], t_step, T_0, period,
    ...  f_c=f_c, f_s=f_s, omdot=omdot, incl=incl, n_grid=801)
    >>> t_zero = T_0 - (time_calc1[0] - (T_0+0.5*p_siderial))/2
    >>> 
    >>> # Now predict times of eclipse
    >>> tmin_calc,lc = ellc.tmin(tmin_obs, t_step, t_zero, period,
    ...  f_c=f_c, f_s=f_s, omdot=omdot, incl=incl, n_grid=101)
    >>> 
    >>> # Print results to screen
    >>> fmt = '{0:.4f} {1:.4f} {2:.4f} {3:8.4f} {4:2s}'
    >>> res = tmin_obs-tmin_calc
    >>> for i in range(0,len(tmin_calc)):
    ...  print fmt.format(tmin_obs[i], tmin_err[i],tmin_calc[i] ,res[i], tmin_type[i])
    >>> 
    >>> # Create a plot
    >>> t_pri = tmin_obs[tmin_type =='Prim']
    >>> e_pri = tmin_err[tmin_type =='Prim']
    >>> c_pri = np.rint((t_pri-t_zero)/p_siderial)
    >>> t_sec = tmin_obs[tmin_type =='Sec']
    >>> e_sec = tmin_err[tmin_type =='Sec']
    >>> c_sec = np.rint((t_sec-t_zero -0.5*p_siderial)/p_siderial) + 0.5
    >>> y_pri = t_pri - (t_zero+p_siderial*c_pri)
    >>> y_sec = t_sec - (t_zero+p_siderial*c_sec)
    >>> plt.figure(star)
    >>> plt.errorbar(c_pri,y_pri,yerr=e_pri,color='b',fmt='o')
    >>> plt.errorbar(c_sec,y_sec,yerr=e_sec,color='r',fmt='o')
    >>> cgrid = np.arange(np.min([c_pri,c_sec])-10,np.max([c_pri,c_sec])+10)
    >>> tfit_pri = tmin_calc[tmin_type =='Prim']
    >>> tfit_sec = tmin_calc[tmin_type =='Sec']
    >>> c_grid = np.arange(np.min([c_pri,c_sec])-100,np.max([c_pri,c_sec])+100)
    >>> c_pri_uniq,i_pri_uniq = np.unique(c_pri, return_index=True)
    >>> spl = InterpolatedUnivariateSpline(c_pri_uniq,tfit_pri[i_pri_uniq])
    >>> t_pri_grid = spl(c_grid)
    >>> c_sec_uniq,i_sec_uniq = np.unique(c_sec, return_index=True)
    >>> spl = InterpolatedUnivariateSpline(c_sec_uniq,tfit_sec[i_sec_uniq])
    >>> t_sec_grid = spl(c_grid)
    >>> plt.plot(c_grid,t_pri_grid - (t_zero+p_siderial*c_grid),color='b')
    >>> plt.plot(c_grid,t_sec_grid - (t_zero+p_siderial*c_grid),color='r')
    >>> plt.xlabel('Cycle')
    >>> plt.ylabel('O-C')
    >>> plt.xlim([np.min([c_pri,c_sec])-100,np.max([c_pri,c_sec])+100])
    >>> plt.show()






  References
  ----------
  .. [1] Maxted, P.F.L. 2016. A fast, flexible light curve model for detached
      eclipsing binary stars and transiting exoplanets. A&A VOLUME, ARTICLE.

  """


  # Copy control parameters into an np.array

  gridname_to_gridsize = {
    "very_sparse" :  4,
    "sparse"       :  8,
    "default"      : 16,
    "fine"         : 24,
    "very_fine"   : 32,
  }
  n1 = gridname_to_gridsize.get(grid_1,None)
  if n1 is None:
    raise Exception("Invalid grid size name")
  n2 = gridname_to_gridsize.get(grid_2,None)
  if n2 is None:
    raise Exception("Invalid grid size name")

  ldstr_to_ldcode = {
    "none"   :  0,
    "lin"    :  1,
    "quad"   :  2,
    "sing"   :  3,
    "claret" :  4,
    "log"    : -1,
    "sqrt"   : -2,
    "exp"    : -3
  }
  if ld_1 is None:
    ldstr_1 = 'none'
  else:
    ldstr_1 = ld_1

  if ld_2 is None:
    ldstr_2 = 'none'
  else:
    ldstr_2 = ld_2

  l1 = ldstr_to_ldcode.get(ldstr_1,None)
  if l1 is None:
    raise Exception("Invalid limb darkening law name")
  l2 = ldstr_to_ldcode.get(ldstr_2,None)
  if l2 is None:
    raise Exception("Invalid limb darkening law name")

  shapename_to_shapecode = {
    "roche"   : -1,
    "sphere"  :  0,
    "poly1p5" :  1,
    "poly3p0" :  2,
  }
  s1 = shapename_to_shapecode.get(shape_1,None)
  if s1 is None:
    raise Exception("Invalid star shape name")
  s2 = shapename_to_shapecode.get(shape_2,None)
  if s2 is None:
    raise Exception("Invalid star shape name")

  if spots_1 is None:
    spar_1 = np.zeros([1,1])
    n_spots_1 = 0
  else:
    spar_1 = np.array(spots_1)
    if (spar_1.ndim != 2) or (spar_1.shape[0] != 4 ):
      raise Exception("spots_1 is not  (4, n_spots_1) array_like")
    n_spots_1 = spar_1.shape[1]

  if spots_2 is None:
    spar_2 = np.zeros([1,1])
    n_spots_2 = 0
  else:
    spar_2 = np.array(spots_2)
    if (spar_2.ndim != 2) or (spar_2.shape[0] != 4 ):
      raise Exception("spots_2 is not  (4, n_spots_2) array_like")
    n_spots_2 = spar_2.shape[1]

  ipar = np.array([n1,n2,n_spots_1,n_spots_2,l1,l2,s1,s2,1],dtype=int)

  # Copy binary parameters into an np.array

  if (radius_1 < 0) or (radius_1 > 1):
    raise ValueError("radius_1 argument out of range")
  if (radius_1 == 1) and (shape_1 != "roche"):
    raise ValueError("radius_1=1 only allowed for Roche potential")

  if (radius_2 < 0) or (radius_2 > 1):
    raise ValueError("radius_2 argument out of range")
  if (radius_2 == 1) and (shape_2 != "roche"):
    raise ValueError("radius_2=1 only allowed for Roche potential")

  par = np.zeros(37)
  par[0] = t_zero
  par[1] = period
  par[2] = sbratio
  par[3] = radius_1
  par[4] = radius_2
  par[5] = incl
  par[6] = 0 # light_3

  if a is not None : par[7] = a

  if (f_c is None) and (f_s is None): 
    pass
  elif (f_c is not None) and (f_s is not None):
    par[8] = f_c
    par[9] = f_s
  else:
    raise Exception("Must specify both f_c and f_s or neither.")

  if q <= 0 :
    raise ValueError("Mass ratio q must be positive.")
  par[10] = q
  
  ld_to_n  = {
    "none"   :  0,
    "lin"    :  1,
    "quad"   :  2,
    "sing"   :  3,
    "claret" :  4,
    "log"    :  2,
    "sqrt"   :  2,
    "exp"    :  2
  }
  ld_n_1 = ldstr_to_ldcode.get(ldstr_1,None)
  try:
    par[11:11+ld_n_1] = ldc_1
  except:
    raise Exception("ldc_1 and ld_1 are inconsistent")
  ld_n_2 = ldstr_to_ldcode.get(ldstr_2,None)
  try:
    par[15:15+ld_n_2] = ldc_2
  except:
    raise Exception("ldc_2 and ld_2 are inconsistent")

  if gdc_1 is not None : par[19] = gdc_1

  if gdc_2 is not None : par[20] = gdc_2

  if didt is not None : par[21] = didt

  if omdot is not None : par[22] = omdot

  par[23] = rotfac_1

  par[24] = rotfac_2

  if bfac_1 is not None : par[25] = bfac_1

  if bfac_2 is not None : par[26] = bfac_2

  if heat_1 is not None : 
    t = np.array(heat_1)
    if t.size == 1:
      par[27] = t
    elif t.size == 3:
      par[27:30] = t
    else:
      raise Exception('Invalid size for array heat_1')

  if heat_2 is not None : 
    t = np.array(heat_2)
    if t.size == 1:
      par[30] = t
    elif t.size == 3:
      par[30:33] = t
    else:
      raise Exception('Invalid size for array heat_2')

  tmin_obs_array = np.array(tmin_obs)
  n_obs = len(tmin_obs_array)
  lc = np.zeros([2,n_obs,n_grid])

  dt_coarse = (np.arange(0,n_grid)-(np.int(2*n_grid+2)/4.-1))*t_step
  for i_obs in range(0,n_obs):
    lc[0,i_obs,:] = tmin_obs_array[i_obs] + dt_coarse
  t_calc = (lc[0,:,:]).reshape(n_obs*n_grid)
  lc_rv_flags = ellc_f.ellc.lc(t_calc,par,ipar,spar_1,spar_2,verbose)
  lc[1,:,:] = (lc_rv_flags[:,0]).reshape(n_obs,n_grid)

  tmin_calc = np.zeros(n_obs)
  n_fine = 100*n_grid
  dt_fine = 0.01*(np.arange(0,n_fine)-(np.int(2*n_fine+2)/4.-1))*t_step
  for i_obs in range(0,n_obs):
    spl = InterpolatedUnivariateSpline(lc[0,i_obs,:], lc[1,i_obs,:])
    t_fine = tmin_obs_array[i_obs] + dt_fine
    f_fine = spl(t_fine)
    i_min = np.argmin(f_fine)
    if (i_min > 0) and (i_min < (len(f_fine)-1)):
      tmin_calc[i_obs] = t_fine[i_min]
    else:
      tmin_calc[i_obs] = np.NaN
        
  return tmin_calc, lc 

