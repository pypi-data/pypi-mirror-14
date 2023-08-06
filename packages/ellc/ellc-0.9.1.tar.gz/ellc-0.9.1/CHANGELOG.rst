0.1.0 (2016-01-07)
~~~~~~~~~~~~~~~~~~
 First version of ellc succesfully installed as a python package

0.2.0 (2016-01-08)
~~~~~~~~~~~~~~~~~~
 Added ellc.tmin() 
 Fixed parameter passing for heat_1, lambda_1, etc. in lc.py and rv.py
 Fixed bub in apsidal motion calculation.

0.3.0 (2016-02-02)
~~~~~~~~~~~~~~~~~~
 Added limb-darkening look-up function ldy.py
 Added examples/ellc_emcee/

0.4.0 (2016-02-02)
~~~~~~~~~~~~~~~~~~
 Minor changes.

0.5.0 (2016-02-06)
~~~~~~~~~~~~~~~~~~
 Minor changes to fortran source files to allow compilation with less tolerant
 version of gfortran.

0.6.0 (2016-02-08)
~~~~~~~~~~~~~~~~~~
 Added lrat as a prior and heating coefficients as variables in ellc_emcee.py.
 Fixed bug in calculation of partial eclipses (uninitialised variables)
 Change contents of examples/ellc_emcee/ to analysis of HD23642.

0.7.0 (2016-02-10)
~~~~~~~~~~~~~~~~~~
 Simplified treatment of reflection.

0.7.1 (2016-02-23)
~~~~~~~~~~~~~~~~~~
 Added ldy to inline doc in __init__.py
 Added astropy requirement to setup.py

0.7.2 (2016-03-22)
~~~~~~~~~~~~~~~~~~
 Added extra output to error message if stars exceed Roche lobes
 Changed ellc_emcee.py so that uniform priors are tested before lc() is called.

0.8.0 (2016-03-28)
~~~~~~~~~~~~~~~~~~
 Fixed bug in printed informtion re: filter names in ellc_emcee.py

0.9.0 (2016-04-19)
~~~~~~~~~~~~~~~~~~
 Removed tmin function.
 Fixed bug in printed information re: filter names in ellc_emcee.py
 Added exact_grav option to lc().
 Improved root polishing in ell_ell_roots function (added do while loop)

0.9.1 (2016-04-19)
~~~~~~~~~~~~~~~~~~
 Removed invalid PKG-INFO entry in MANIFEST.in
