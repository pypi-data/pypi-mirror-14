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
import corner
import matplotlib.pyplot as plt
from astropy.table import Table, Column

#------------------------------------------------------------------------------

# Handy class for printing floats...
class prettyfloat(float):
  def __repr__(self):
    return "%0.6f" % self

#------------------------------------------------------------------------------
# Generate plots

chain = Table.read('chain.csv')
chain = Table(chain, masked=True)

nwalkers = 1+np.max(chain['walker'])
nsteps = 1+np.max(chain['step'])
print('Read chain.csv with {:d} walkers of {:d} steps'
    .format(nwalkers,nsteps))

chisq =  -2*chain['loglike']
chisq_median =  np.median(chisq)
chisq_mad =  np.median(np.abs(chisq - np.median(chisq)))
chisq_tol = chisq_median + 3*chisq_mad
print ('Median chi-squared over all walkers = {:9.1f}'.format(chisq_median))
print ('Median absolute deviation of chi-squared over all walkers = {:9.1f}'
    .format(chisq_mad))
mask = chisq > chisq_tol
nok = len(chain) - len(mask.nonzero()[0])
print ('Calculating results for {:d} steps with  chi-squared < {:9.1f}'.
    format(nok,chisq_tol))
chain.remove_column('step')
chain.remove_column('walker')
chain.remove_column('loglike')
lrat = chain['sb2']*(chain['r_2']/chain['r_1'])**2
chain.add_column(Column(lrat,name='lrat'))

ndim = len(chain.colnames)
for colname in chain.colnames:
  p =  np.extract(mask == False,chain[colname])
  if colname == 'T_0' :
    print('{:s} = {:14.6f} +/- {:8.6f}'.format(colname, 
      np.median(p),  np.std(p)))
  elif colname == 'P' :
    print('{:s} = {:12.8f} +/- {:10.8f}'.format(colname, 
      np.median(p),  np.std(p)))
  else:
    print('{:s} = {:10.6g} +/- {:10.6g}'.format(colname, 
      np.median(p),  np.std(p)))

colnames_plot = ['r_1','r_2','incl','sb2','lrat']
labels_plot = ['$r_1$','$r_2$','$i [^{\circ}]$','$s$','$l_2/l_1$']
nplot = len(colnames_plot)
medians = np.zeros(nplot)
samples = np.zeros([nok,nplot])
for ii,colname in enumerate(colnames_plot) :
  p =  np.extract(mask == False,chain[colname])
  samples[:,ii] = p
  medians[ii] = np.median(p)

# Results from Trevor et al., arXiv:1602.01901v1
previous = [0.1450, 0.1262, 78.21, 0.4859, 0.355]
# Plot parameter distributions
fig_p = corner.corner(samples, labels=labels_plot, truths=previous)
if args.eps:
  fig_p.savefig("corner.eps")
else:
  plt.show()



