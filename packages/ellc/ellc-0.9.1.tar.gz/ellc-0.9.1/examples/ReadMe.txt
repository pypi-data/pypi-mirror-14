
Scripts to generate plots for Maxted, 2016 A&A VOLUME, ARTICLE.

 The executable file ".py" file in each folder/sub-directory will, by default,
produce a screen plot of the results. To produce the .eps file add the
optional argument to the command "--eps", e.g., 
$ ./KPD1946+4340  --eps

batman/
run_batman.py - Generate plot to compare ellc to batman
batman.eps    - output from run_batman.py
                  
DoublePartial/ 
DoublePartial.py   - Generate plot to compare ellc to Nightfall 
DoublePartial.cfg  - Nightfall input file 
NightfallCurve.dat - From "nightfall -C DoublePartial.cfg -R1 -F -M -N1000"
DoublePartial.eps  - Output from DoublePartial.py

ellc_emcee/
ellc_emcee.py - Interactive script for fitting a single light curve.
HD23642.in    - Example input to ellc_emcee.py - light curve of HD23642
HD23642.dat   - Kepler K2 light curve for HD23642
HD23642.log   - ./ellc_emcee.py -g very_sparse -l HD23642.log < HD23642.in
chain.csv     - Output emcee chain from same command (this takes some time...)
model.csv     - Output model light curve from same command
plot_chain.py - Compare selected parameters to results in arXiv:1602.01901v1
corner.eps    - Output from plot_chain.py
plot_lcfit.py - Plot model fit to light curve
lcfit.eps     - Output from plot_lcfit.py


GD448/
GD448.py           - Generate plot to compare ellc to Nightfall for GD448
GD448.cfg          - Nightfall input file
NightfallCurve.dat - From "nightfall -N1000 -F -C GD448.cfg -OP 5 -M -R9"
GD448.eps          - Output from GD448.py  
 
J0113+31/
J0113+31.py  - Analysis of J0113+31 using ellc  (this takes some time...)
table*.dat   - Data from Gomez Maqueo Chew et al., 2014A&A...572A..50G
J0113+31.eps - Output from J0113+31.py - light curve plots
corner.eps   - Output from J0113+31.py - parameter correlation plots

KPD1946+4340/
KPD1946+4340.py   - Comparison of ellc model to Kepler data for KPD1946+4340
kplr007975824.dat - Phase-binned short-cadence Kepler data for KPD1946+4340
KPD1946+4340.eps  - Output from KPD1946+4340.py

KSint/
KSint.py   - Generate plot to compare ellc to KSint
inputs.txt - KSint input file
lc.dat     - Output from KSint
KSint.eps  - Output from KSint.py

PhotRM/
PhotRM.py  - Generate plot of the photometric R-M effect using ellc
PhotRM.eps - Output from PhotRM.py
