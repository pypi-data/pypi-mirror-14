! This file is part of the ellc binary star model
! Copyright (C) 2016 Pierre Maxted
! 
! This program is free software: you can redistribute it and/or modify
! it under the terms of the GNU General Public License as published by
! the Free Software Foundation, either version 3 of the License, or
! (at your option) any later version.
! 
! This program is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.
! 
! You should have received a copy of the GNU General Public License
! along with this program.  If not, see <http://www.gnu.org/licenses/>.

module stellar
! Stellar astrophysics functions for ellc
!
! HISTORY
! -------
! Apr 2016
! Added exact_grav option to bright
! p.maxted@keele.ac.uk
!
! Jan 2016
! First version 
! p.maxted@keele.ac.uk
!
!
use constants
use utils

implicit none

! Routines for calculating geometry
public starshape     ! Ellipsoidal approximation to shape of a body in a binary
public roche         ! Roche potential from  Wilson, 1979ApJ...234.1054
public roche_l1      ! Position of the inner Lagrangian point
public droche        ! Derivative of Roche potential 
! Stellar surface flux distribution
public limbdark      ! Limb darkening laws
public bright        ! Stellar surface brightness and/or rad. vel.
public ld_quad_match ! Quadratic coefficients to match another limb darking law
public gmodel_coeffs ! Calculate coeffs of surface gravity approximating func.
! Keplerian orbits
public eanom         ! Eccentric anomaly from mean anomaly
public trueanom      ! True anomaly from mean anomaly
public t_ecl_to_peri ! Time of periastron passage prior to a time of eclipse.
public delta_func    ! Helper function for t_ecl_to_peri

contains

function starshape(radius, rsep, frot, ecc, qmass, model, rtol, &
                   verbose) result(abcd)
implicit none
! Semi-major axes (A,B,C) and offset towards companion, D, from centre-of-mass
! to geometrical centre of an ellipsoid that approximates the shape of a
! star in a binary system. 
!
! All quantities measured in units of semi-major axis of binary.
! A = semi-major axis on x-axis towards companion
! B = semi-major axis in orbital plane perpendicular to x-axis
! C = semi-major axis on an axis perpendicular to orbital angular momentum
!     vector
!
! Rotation and orbital angular momentum vectors are assumed parallel.
!
! For invalid input all return values are set to bad_dble
!
! Polytropic models use rotational distortion from interpolation in Table 1 of
! James, 1964ApJ...140..552J.
!
! Tidal distortion for polytropes is from Chandrasekhar, 1933MNRAS..93..449C.
!
! Tidal and rotational distortion are assumed to be independent.
!
! The definition of the Roche potential is from Wilson, 1979ApJ...234.1054W
! 
! RADIUS= Radius of a sphere with the same volume as the ellipsoid to be
!         calculated. For the Roche model only, set radius=1 to specify
!         a star that fills its Roche lobe.
! RSEP  = Separation of the stars in units of the semi-major axis.
! FROT  = angular velocity of star/pseudo-synchronous angular velocity
! ECC   = eccentricity
! QMASS = mass of companion/mass of star
! RTOL  = Tolerance on fractional difference (ABC**(1/3)-radius)/radius.
!         If RTOL <= EPSILON(0.0), e.g., 0.0, then EPSILON(0.0) 
!         (machine precision) is used as the tolerance.
!
! MODEL = -1 - Roche model
!       =  0 - spherical star
!       =  1 - polytrope n = 1.5
!       =  2 - polytrope n = 3
!
! VERBOSE : 0 = silent
!           1 = error messages
!           2 = warning messages
!           3 = informational messages
!           4 = debugging
!
!-

double precision, intent(in) :: radius  ! Radius of a sphere with the same volume as the ellipsoid
double precision, intent(in) :: rsep    ! Separation of the stars in units of the semi-major axis
double precision, intent(in) :: frot    ! angular velocity of star/pseudo-synchronous angular velocity
double precision, intent(in) :: ecc     ! eccentricity of the orbit
double precision, intent(in) :: qmass   ! mass of companion/mass of star
double precision, intent(in) :: rtol    ! Tolerance on fractional difference (ABC**(1/3)-radius)/radius
integer, intent(in)  :: model   ! Model used to calculate star shape (see constants)
integer, intent(in)  :: verbose ! Verbosity level for error reporting
double precision             :: abcd(4) ! semi-major axis on x-axis towards companion

! Local variables
double precision ::  rt, t, ttol, tlo, thi
double precision ::  a,b,c,d
double precision ::  rsep_l

if(verbose >= v_debug) then
  print *,'starshape: radius, q, ecc, rsep, model = ', &
  radius,qmass,ecc,rsep,model
end if 
if ((radius <= 0.d0).or.(radius.gt.1.d0))then
  a = bad_dble
  b = bad_dble
  c = bad_dble
  d = bad_dble
  if(verbose >= v_error)then
    print *,'starshape: error: invalid input radius: ',radius
  end if
  return
end if

! If rsep is within 4*epsilon(0.d0) of 1-ecc or 1+ecc then assume that this
! is due to round-off error 
! Use rsep_l as a local copy of rsep which is within the allowed range.
tlo = rsep - (1.d0-ecc)
thi = (1.d0+ecc) - rsep
ttol = 4.0d0*epsilon(0.d0)
if ((tlo > 0).and.(thi > 0)) then
  rsep_l = rsep
else if (abs(tlo) < ttol) then
  rsep_l = (1.d0-ecc)
else if (abs(thi) < ttol) then
  rsep_l = (1.d0+ecc)
else
  a = bad_dble
  b = bad_dble
  c = bad_dble
  d = bad_dble
  if(verbose >= v_error)then
    print *,'starshape: error: rsep out of range: ', rsep,ecc
  end if
  return
endif

ttol = max(rtol, epsilon(0.d0))
rt = radius

select case (model)

case(starshape_roche)

  t = 1.d0
  do while (t.gt.ttol)
    call shape_roche(rt,rsep_l,frot,qmass,a,b,c,d,verbose-1)
    if(d.eq.bad_dble) return
    if (radius.eq.1.d0) then
      t = 0.d0
    else
      t = (a*b*c)**third/radius
      rt = rt/t
      t = abs(t-1.d0)
    end if
  end do

case(starshape_sphere)

  a = radius
  b = radius
  c = radius
  d = 0.d0
  t = 0.d0

case(starshape_poly1p5)

  t = 1.d0
  do while (t.gt.ttol)
    call shape_n1p5(rt,rsep_l,frot,ecc,qmass,a,b,c,d,verbose-1)
    if(d.eq.bad_dble) return
    t = (a*b*c)**third/radius
    rt = rt/t
    t = abs(t-1.d0)
  end do

case(starshape_poly3p0)

  t = 1.d0
  do while (t.gt.ttol)
    call shape_n3p0(rt,rsep_l,frot,ecc,qmass,a,b,c,d,verbose-1)
    if(d.eq.bad_dble) return
    t = (a*b*c)**third/radius
    rt = rt/t
    t = abs(t-1.d0)
  end do

case default
  a = bad_dble
  b = bad_dble
  c = bad_dble
  d = bad_dble
  if(verbose >= v_error) then
    print *,'starshape: error: invalid input model'
  end if
  return

end select

if(verbose >= 4) print *,'starshape: normal exit : a,b,c,d,t  = ',a,b,c,d,t

abcd = (/a, b, c, d/)
return

end function starshape

!-----------------------------------------------------------------------

subroutine shape_n1p5(radius,rsep,frot,ecc,qmass,a,b,c,d,verbose)
implicit none
double precision, intent(in)  :: radius, rsep, frot, ecc, qmass
double precision, intent(out) :: a, b, c, d
integer, intent(in)           :: verbose

! Local variables
integer, parameter :: npar = 1
double precision   :: ar, par(npar), a1, a2, w
double precision   :: dxip,dxie
double precision   :: dsig0
double precision   :: qnu3,qnu4,qnu5
integer            :: ii
double precision, parameter :: delta2=1.2892d0
double precision, parameter :: delta3=1.1079d0
double precision, parameter :: delta4=1.0562d0
double precision, parameter :: tol = 1.0d-6

! These fractional changes in polar and equatorial radii and 
! fraction change in volume equivalent radius based on columns xi_p, xi_e and
! 10^-2V in Table 1 of James, 1964
!
double precision tdxip(25),tdxie(25)
data tdxip/ &
 0.0000000d0,-0.0042422d0,-0.0084843d0,-0.0127265d0,-0.0169960d0, &
-0.0212929d0,-0.0255898d0,-0.0298867d0,-0.0342383d0,-0.0385900d0, &
-0.0429690d0,-0.0473753d0,-0.0518091d0,-0.0562976d0,-0.0607860d0, &
-0.0653293d0,-0.0699272d0,-0.0745525d0,-0.0792510d0,-0.0840221d0, &
-0.0888390d0,-0.0927801d0,-0.0947780d0,-0.0968033d0,-0.0978160d0/ 
data tdxie/ &
0.00000000d0,0.00747167d0,0.01524440d0,0.02331819d0,0.03174777d0, &
0.04056051d0,0.04981116d0,0.05949970d0,0.06970825d0,0.08046417d0, &
0.09190432d0,0.10408342d0,0.11713832d0,0.13117850d0,0.14642290d0, &
0.16311785d0,0.18161914d0,0.20250151d0,0.22653128d0,0.25521375d0, &
0.29153210d0,0.33124418d0,0.35885927d0,0.40092506d0,0.45073622d0/

par(1) = frot**2 * radius**3 * (1.d0+qmass) * (1.d0-ecc**2) / (1.d0-ecc)**4

a1 = 0.d0
a2 = 1.09d-2
ar =  zbrent(func_n1p5,a1,a2,tol,npar,par,verbose-1)
if(verbose >= v_debug) print *,'shape_n1p5: ar =',ar
if (ar < 0.d0) then
  a = bad_dble
  b = bad_dble
  c = bad_dble
  d = bad_dble
  if(verbose >= v_error) print *,'shape_n1p5: radius out of range.',radius,frot,ecc,qmass
  return
end if

! Interpolate values of fractional changes in radius
if(ar < 1.0d-2) then
  w = 0.2d4*ar
  ii = 1+int(w)
  w = dble(ii)-w
  dxip = w*tdxip(ii) + (1.d0-w)*tdxip(ii+1)
  dxie = w*tdxie(ii) + (1.d0-w)*tdxie(ii+1)
else if(ar < 1.04d-2) then
  w = 0.25d4*(ar-1.0d-2)
  dxie = (1.d0-w)*tdxie(21) + w*tdxie(22)
  dxip = (1.d0-w)*tdxip(21) + w*tdxip(22)
else if(ar <= 1.08d-2) then
  w = 0.5d4*(ar-1.04d-2)
  ii = 22+int(w)
  w = dble(ii-21)-w
  dxie = w*tdxie(ii) + (1.d0-w)*tdxie(ii+1)
  dxip = w*tdxip(ii) + (1.d0-w)*tdxip(ii+1)
else if(ar <= 1.09d-2) then
  w = ar-1.08d-2
  dxie = (1.d0-w)*tdxie(24) + w*tdxie(25)
  dxip = (1.d0-w)*tdxip(24) + w*tdxip(25)
else
  print *,'shape_n1p5: invalid value of ar',ar
  stop
end if

a = radius*(1.d0+dxie)
b = a
c = radius*(1.d0+dxip)

! Tidal distortion
ar = radius/rsep
qnu3 = qmass*ar**3 
qnu4 = qnu3*ar
qnu5 = qnu4*ar
a = a*(1.d0 + 0.5d0*(delta2*qnu3+delta4*qnu5))
dsig0 = 1.d0 - 0.5d0*delta2*qnu3 + 0.375d0*delta4*qnu5
b = b*dsig0
c = c*dsig0
d = delta3*qnu4*radius

return

end subroutine shape_n1p5

!-----------------------------------------------------------------------

double precision function func_n1p5(a,npar,par,verbose)
implicit none
!
! par(1) = f^2 * (1+q) * r_v**3 * (1.d0-ecc**2)/(1.d0-ecc)**4
! 
integer, intent(in)          :: npar, verbose
double precision, intent(in) :: a, par(npar)

! Local variables
double precision array(25)
integer ii
double precision w

! The values in this array are 2*pi*m/3*v where m and v are from Table 1 of
! James, 1964ApJ...140..552J. Return value is linear interpolation in this
! table multiplied by par(1) then subtracted from a
! Out-of range values returned as bad_dble
data array/ &
0.02782105d0,0.02768557d0,0.02754373d0,0.02739694d0,0.02724204d0, &
0.02708024d0,0.02691018d0,0.02673288d0,0.02654358d0,0.02634414d0, &
0.02613295d0,0.02590672d0,0.02566646d0,0.02540777d0,0.02512701d0, &
0.02482182d0,0.02448562d0,0.02410966d0,0.02368468d0,0.02319031d0, &
0.02259155d0,0.02198336d0,0.02160056d0,0.02109994d0,0.02071318d0/

if (verbose > v_debug) print *,'func_n1p5: a =', a

if(a < 0.d0) then
  func_n1p5 = bad_dble
else if(a < 1.0d-2) then
  w = a/0.05d-2
  ii = 1+int(w)
  w = dble(ii)-w
  func_n1p5 = a-par(1)*(w*array(ii) + (1.d0-w)*array(ii+1))
else if(a < 1.04d-2) then
  w = (a-1.0d-2)/0.04d-2
  func_n1p5 = a-par(1)*((1.d0-w)*array(21) + w*array(22))
else if(a <= 1.08d-2) then
  w = (a-1.04d-2)/0.02d-2
  ii = 22+int(w)
  w = dble(ii-21)-w
  func_n1p5 = a-par(1)*(w*array(ii) + (1.d0-w)*array(ii+1))
else if(a <= 1.09d-2) then
  w = a-1.08d-2
  func_n1p5 = a-par(1)*((1.d0-w)*array(24) + w*array(25))
else
  func_n1p5 = bad_dble
end if
return

end function func_n1p5

!-----------------------------------------------------------------------

subroutine shape_n3p0(radius,rsep,frot,ecc,qmass,a,b,c,d,verbose)
implicit none
double precision, intent(in)  :: radius, rsep, frot, ecc, qmass
double precision, intent(out) :: a, b, c, d
integer, intent(in)           :: verbose

! Local variables
integer, parameter :: npar = 1
double precision   :: ar, par(npar), a1, a2, w
double precision   :: dxip,dxie
double precision   :: dsig0
double precision   :: qnu3,qnu4,qnu5
integer            :: ii
double precision, parameter :: delta2=1.0289d0
double precision, parameter :: delta3=1.00736d0
double precision, parameter :: delta4=1.00281d0
double precision, parameter :: tol = 1.0d-6

! These fractional changes in polar and equatorial radii and 
! fraction change in volume equivalent radius based on columns xi_p, xi_e and
! 10^-2v in table 1 of James, 1964
!
double precision tdxip(24),tdxie(24)
data tdxip/ &
 0.0000000d0,-0.0015862d0,-0.0031623d0,-0.0047471d0,-0.0063333d0, &
-0.0079138d0,-0.0094956d0,-0.0110731d0,-0.0126667d0,-0.0142500d0, &
-0.0158232d0,-0.0174036d0,-0.0189855d0,-0.0205674d0,-0.0221536d0, &
-0.0237558d0,-0.0253406d0,-0.0269311d0,-0.0285232d0,-0.0291582d0, &
-0.0297919d0,-0.0301109d0,-0.0304298d0,-0.0307503d0/
data tdxie/ &
0.00000000d0,0.00692635d0,0.01416734d0,0.02175631d0,0.02972951d0, &
0.03812610d0,0.04700117d0,0.05640546d0,0.06641728d0,0.07712796d0, &
0.08861727d0,0.10106498d0,0.11461754d0,0.12951130d0,0.14608118d0, &
0.16478972d0,0.18633434d0,0.21185324d0,0.24351697d0,0.25880946d0, &
0.27637255d0,0.28627707d0,0.29714145d0,0.30924118d0/

par(1)=frot**2 * radius**3 * (1.d0+qmass) * (1.d0-ecc**2)/(1.d0-ecc)**4
a1 = 0.d0
a2 = 9.7d-4
ar =  zbrent(func_n3p0,a1,a2,tol,npar,par,verbose-1)
if(verbose >= v_debug) print *,'shape_n3p0: ar =',ar
if (ar < 0.d0) then
  a = bad_dble
  b = bad_dble
  c = bad_dble
  d = bad_dble
  if(verbose >= 1) print *,'shape_n3p0: radius out of range.',radius,frot,ecc,qmass
  return
end if

! Interpolate values of fractional changes in radius
if(ar.lt.9.0d-4) then
  w = ar/0.5d-4
  ii = 1+int(w)
  w = dble(ii)-w
  dxip = w*tdxip(ii) + (1.d0-w)*tdxip(ii+1)
  dxie = w*tdxie(ii) + (1.d0-w)*tdxie(ii+1)
else if(ar.lt. 9.4d-4) then
  w = (a-9.0d-4)/0.2d-4
  ii = 19+int(w)
  w = dble(ii-18)-w
  dxip = w*tdxip(ii) + (1.d0-w)*tdxip(ii+1)
  dxie = w*tdxie(ii) + (1.d0-w)*tdxie(ii+1)
else if(ar <= 9.7d-4) then
  w = (a-9.4d-4)/0.1d-4
  ii = 21+int(w)
  w = dble(ii-20)-w
  dxip = w*tdxip(ii) + (1.d0-w)*tdxip(ii+1)
  dxie = w*tdxie(ii) + (1.d0-w)*tdxie(ii+1)
else
  print *,'shape_n3p0: invalid value of ar',ar
  stop
end if
a = radius*(1.d0+dxie)
b = a
c = radius*(1.d0+dxip)

! Tidal distortion
ar = radius/rsep
qnu3 = qmass*ar**3 
qnu4 = qnu3*ar
qnu5 = qnu4*ar
a = a*(1.d0 + 0.5d0*(delta2*qnu3+delta4*qnu5))
dsig0 = 1.d0 - 0.5d0*delta2*qnu3 + 0.375d0*delta4*qnu5
b = b*dsig0
c = c*dsig0
d = delta3*qnu4*radius

return

end subroutine shape_n3p0

!-----------------------------------------------------------------------

double precision function func_n3p0(a,npar,par,verbose)
implicit none
!
! par(1) = f^2 * (1+q) * r_v**3 * (1.d0-ecc**2)/(1.d0-ecc)**4
! 
integer, intent(in)          :: npar, verbose
double precision, intent(in) :: a, par(npar)

! Local variables
double precision array(24)
integer ii
double precision w
! The values in this array are 2*pi*m/3*v where m and v are from table 1 of
! james, 1964apj...140..552j. Return value is linear interpolation in this
! table multiplied by par(1) then subtracted from a
! out-of range values returned as bad_dble
data array/ &
0.00307603d0,0.00304253d0,0.00300812d0,0.00297269d0,0.00293619d0, &
0.00289851d0,0.00285958d0,0.00281926d0,0.00277739d0,0.00273384d0, &
0.00268838d0,0.00264078d0,0.00259069d0,0.00253778d0,0.00248146d0, &
0.00242103d0,0.00235546d0,0.00228318d0,0.00220144d0,0.00216504d0, &
0.00212572d0,0.00210468d0,0.00208254d0,0.00205903d0/

if (verbose > v_debug) print *,'func_n1p5: a =', a

if(a < 0.d0) then
  func_n3p0 = bad_dble
else if(a < 9.0d-4) then
  w = a/0.5d-4
  ii = 1+int(w)
  w = dble(ii)-w
  func_n3p0 = a-par(1)*(w*array(ii) + (1.d0-w)*array(ii+1))
else if(a < 9.4d-4) then
  w = (a-9.0d-4)/0.2d-4
  ii = 19+int(w)
  w = dble(ii-18)-w
  func_n3p0 = a-par(1)*(w*array(ii) + (1.d0-w)*array(ii+1))
else if(a <=  9.7d-4) then
  w = (a-9.4d-4)/0.1d-4
  ii = 21+int(w)
  w = dble(ii-20)-w
  func_n3p0 = a-par(1)*(w*array(ii) + (1.d0-w)*array(ii+1))
else
  func_n3p0 = bad_dble
end if
return
end function func_n3p0

!-----------------------------------------------------------------------

subroutine shape_roche(radius,rsep,frot,qmass,a,b,c,d,verbose)
implicit none

double precision, intent(in)  :: radius, rsep, frot, qmass
double precision, intent(out) :: a, b, c, d
integer, intent(in)           ::  verbose

! Local variables
double precision   :: pot, a1,  rl1
integer, parameter :: npar = 4
double precision   :: par(npar)
double precision, parameter :: tol=1.0d-9

rl1 = roche_l1(qmass,frot)
if (radius == 1.d0) then
  a = rl1
else
  if (radius > rl1) then
    if(verbose >= v_error) then
      print *,' shape_roche: star exceeds roche lobe'
      print *,' shape_roche: radius,rl1,q = ',radius,rl1,qmass
    end if
    a = bad_dble
    b = bad_dble
    c = bad_dble
    d = bad_dble
    return
  end if
  a = radius
end if
pot = roche(a,0.d0,0.d0,rsep,qmass,frot)
par(1) = pot
par(2) = rsep
par(3) = qmass
par(4) = frot
b = zbrent(func_b,a*0.5d0,a*1.1d0,tol,npar,par,verbose-1)
c = zbrent(func_c,a*0.5d0,a*1.1d0,tol,npar,par,verbose-1)
a1 = zbrent(func_a,-a*1.5d0,-a*0.5d0,tol,npar,par,verbose-1)
d = 0.5*(a1+a)
a = a - d

end subroutine shape_roche

!-----------------------------------------------------------------------

double precision function func_a(a,npar,par,verbose)
implicit none
integer, intent(in)          :: npar, verbose
double precision, intent(in) :: a, par(npar)
if (verbose > v_debug) print *,'func_a: ', a
func_a=par(1)-roche(a,0.d0,0.d0,par(2),par(3),par(4))
return 
end function func_a

!-----------------------------------------------------------------------

double precision function func_b(b,npar,par,verbose)
implicit none
integer, intent(in)          :: npar, verbose
double precision, intent(in) :: b, par(npar)
if (verbose > v_debug) print *,'func_b: ', b
func_b = par(1)-roche(0.d0,b,0.d0,par(2),par(3),par(4))
return 
end function func_b

!-----------------------------------------------------------------------

double precision function func_c(c,npar,par,verbose)
implicit none
integer, intent(in)          :: npar, verbose
double precision, intent(in) :: c, par(npar)
if (verbose > v_debug) print *,'func_c: ', c
func_c=par(1)-roche(0.d0,0.d0,c,par(2),par(3),par(4))
return 
end function func_c

!-----------------------------------------------------------------------

double precision function roche(x, y, z, d, q, f, iscomp)
!+
!
! Roche potential according to the definition of Wilson, 1979ApJ...234.1054W
!
! Input position is (X, Y, Z)
!  - origin at centre-of-mass of the star.
!  - x-axis towards companion
!  - y-axis in orbtial plane opposite to direction of orbital motion
!  - z-axis parallel to orbital angular momentum vector
!  - all lengths relative to the semi-major axis of the binary.
! 
! Q is mass ratio = mass companion/mass of star.
!
! D is instantaneous separation of the centres.
!
! F is the synchronization index of the star, i.e. the ratio of sidereal 
! rotational and orbital frequency
!
! To evaluate the potential for the companion to a star with consistent
! units for two stars:
!  - set "ISCOMP" to .TRUE.
!  - Use the value of F appropriate for the companion
!  - Measure position from the centre of the companion with x-axis
!    towards the star
!  - Use mass ratio Q = mass of companion/mass star, as before.
!  
! Invalid input returns the values bad_dble
!
! p.maxted@keele.ac.uk, Jun 2015 
!
!-
implicit none
double precision, intent(in)  :: q       ! mass ratio = mass of companion/mass of star
double precision, intent(in)  :: x, y, z ! position (x, y, z) at which to evaluate the function
double precision, intent(in)  :: d       ! instantaneous separation of the stars
double precision, intent(in)  :: f       ! synchronization index of the star
logical, intent(in), optional :: iscomp  ! Set .true. to calculate potential due to companion star

! Local variables
double precision qq, r, r2, nu, lam, d2
logical iscomp_l

if (present(iscomp)) then
  iscomp_l = iscomp
else
  iscomp_l = .false.
end if

if (q <= 0.d0) then
  roche = bad_dble
  return
end if

if (iscomp_l) then
  qq = 1.d0/q
else
  qq = q
end if

r2 = x**2 + y**2 + z**2
if (r2 == 0.d0) then
  roche = bad_dble
  return
end if

r = sqrt(r2)
nu = z/r
lam = x/r
d2 = d**2
roche = 1.d0/r + qq*( 1.d0/sqrt(d2+r2-2.0d0*r*lam*d) - r*lam/d2 ) &
+ 0.5d0 * f**2 * (1.d0+qq) * r2 * (1.d0-nu**2) 
if (iscomp_l) roche = roche/qq + 0.5d0*(qq-1.d0)/qq

return
end function roche

!-----------------------------------------------------------------------

double precision function roche_l1(q, f)
implicit none
double precision, intent(in) ::  q   ! (mass of companion) / (mass of star)  
double precision, intent(in),optional ::  f   ! Rotation factor
!+
!
! Position of the inner Lagrangian point in terms of the separation of 
! two stars which have mass ratio, q.
! Works by solving for root of a quintic polynomial, by Newton-Raphson
! iteration
! Q = (mass of companion) / (mass of star)
! L1 = (distance from centre of star to inner Lagrangian point)/separation
!
! Optional input factor f is the asynchronous rotation factor as defined by
! Wilson, 1979ApJ...234.1054W
!
! For invalid input return value is bad_dble
!
!-
double complex   ::  az(6) = (/ &
   dcmplx(-1.d0,0.0d0),dcmplx(2.0d0,0.0d0),dcmplx(-1.d0,0.0d0), &
   dcmplx(0.d0,0.0d0),dcmplx(0.0d0,0.0d0),dcmplx(0.d0,0.0d0) /)
double complex   ::  z
integer ::  m
double precision :: fac

if(q <= 0.d0) then
  roche_l1 = bad_dble
  return
end if

if (present(f)) then 
  fac = f**2*(1.0d0+q)
  az(4) =dcmplx( fac + 2.0d0*q,0.0d0)
  az(5) =dcmplx(-2.0d0*fac - q,0.0d0)
  az(6) =dcmplx( fac          ,0.0d0)
else
  az(4) =dcmplx( 1.0d0 + 3.0d0*q,0.0d0)
  az(5) =dcmplx(-2.0d0 - 3.0d0*q,0.0d0)
  az(6) =dcmplx( 1.0d0 + q      ,0.0d0)
end if
z     =dcmplx( 1.0d0/(1.0d0+q),0.0d0)
m=5
roche_l1 = dble(laguerre(az,m,z))
return

end function roche_l1

!-----------------------------------------------------------------------

double precision function droche(q, x, y, z, d, f)
!+
!  Evaluates magnitude of the derivative of the dimensionless Roche potential
! at a point X,Y,Z measured from the centre of mass of the star in units of
! the semi-major axis of the binary.
!
! D = instantaneous separation of the stars. 
!
! Q = mass ratio = mass of companion/mass of star.
!
! F = synchronization index of the star, i.e. the ratio of sidereal 
!     rotational and orbital frequency
! 
! Roche potential according to the definition of Wilson, 1979ApJ...234.1054W
!
! Invalid input returns the values bad_dble
!
! p.maxted@keele.ac.uk, Jun 2015 
!
!-
implicit none
double precision, intent(in) :: q       ! mass ratio = mass of companion/mass of star
double precision, intent(in) :: x, y, z ! position (x, y, z) at which to evaluate the function
double precision, intent(in) :: d       ! instantaneous separation of the stars
double precision, intent(in) :: f       ! synchronization index of the star

! Local variables
double precision domx,domy,domz
double precision t1, t2, f21q

if (d <= 0.d0) then
  droche = bad_dble
  return
end if

t1 = x**2 + y**2 + z**2
if (t1 == 0.d0) then
  droche = bad_dble
  return
end if
t1 = t1**(-1.5d0)

t2 = (d-x)**2 + y**2 + z**2
if (t2 == 0.d0) then
  droche = bad_dble
  return
end if
t2 = q*t2**(-1.5d0)

f21q = f**2*(1.d0+q)

domx = -x*t1 + (d-x)*t2 + f21q*x - q/d**2
domy = -y*(t1 + t2 - f21q)
domz = -z*(t1 + t2)
droche = sqrt(domx**2 + domy**2 + domz**2)
return
end function droche

!-------------------------------------------------------------------------------

double precision function limbdark(mu, law, ldc)
! Limb darkening
implicit none
double precision,intent(in) :: mu     ! Cosine of the viewing angle
double precision,intent(in) :: ldc(:) ! Limb darkening coefficients
integer, intent(in) :: law    ! Limb darkening law - see constants.f90

select case (law)

case(ld_none) ! no limb darkening
  limbdark = 1.d0
  return

case(ld_linear) ! linear
  limbdark = 1.d0 - ldc(1)*(1.d0-mu)
  return

case(ld_quadratic) ! quadratic
  limbdark = 1.d0 - ldc(1)*(1.d0-mu) - ldc(2)*(1.d0-mu)**2
  return

case(ld_sing) ! sing 3-parameter
  limbdark = 1.d0 - ldc(1)*(1.d0-mu) - ldc(2)*(1.d0-mu**1.5d0) &
           - ldc(3)*(1.d0-mu**2)
  return

case(ld_claret) ! claret 4-parameter
  limbdark = 1.d0 - ldc(1)*(1.d0-sqrt(mu)) - ldc(2)*(1.d0-mu) &
           - ldc(3)*(1.d0-mu**1.5d0)- ldc(4)*(1.d0-mu**2)
  return

case(ld_logarithmic) ! logarithmic
  limbdark = 1.d0 - ldc(1)*(1.d0-mu) - ldc(2)*mu*log(mu)
  return

case(ld_square_root) ! square-root
  limbdark = 1.d0 - ldc(1)*(1.d0-mu) - ldc(2)*(1.d0-sqrt(mu))
  return

case(ld_exponential) ! exponential
  limbdark = 1.d0 - ldc(1)*(1.d0-mu) - ldc(2)/(1.d0-exp(mu))
  return
case default ! 
  limbdark = bad_dble
end select

end function limbdark

!-------------------------------------------------------------------------------

function ld_quad_match(law, ldc) result(ldc_q) 
! Set coefficients of a quadratic limb darkening law so that the intensity
! profile matches at mu= 0, 0.5, 1.0
! N.B.  these are the coefficients on the quadratic limb darkening law as used
! in eker, i.e.,  I_0[1 - u_1.mu + u_2.mu^2], so u_2 is the negative of the
! normal quadratic limb darkening coefficient.
implicit none
integer, intent(in) :: law    ! Limb darkening law - see constants.f90
double precision,intent(in) :: ldc(:)    ! Limb darkening coefficients
double precision            :: ldc_q(2) ! Quadratic limb darkening coefficients

double precision :: x0, x1

select case (law)

case(ld_none) ! no limb darkening
  ldc_q = (/ 0.0d0, 0.0d0 /)
  return

case(ld_linear) ! linear
  ldc_q = (/ ldc(1), 0.0d0 /)
  return

case(ld_quadratic) ! quadratic
  ldc_q = (/ ldc(1), -ldc(2) /)
  return

case default ! other
  x0 = limbdark(0.0d0, law, ldc)
  x1 = limbdark(0.5d0, law, ldc)
  ldc_q = (/ 3.0d0 - 4.0d0*x1 + x0, -4.0d0*x1 + 2.0d0*x0 + 2.0d0 /)
  return
end select

end function ld_quad_match
        
!-------------------------------------------------------------------------------
function gmodel_coeffs(abcd, rsep, frot, qmass,  verbose) result(gmodel) 
implicit none
double precision,intent(in) :: abcd(4)
double precision,intent(in) :: rsep  
double precision,intent(in) :: frot  
double precision,intent(in) :: qmass
integer, intent(in)         :: verbose
double precision :: gmodel(3)

! Local variables
double precision,parameter  :: rtol = 0.0d0
double precision  :: gpole,gside,gback,gfront
double precision  :: ax(3),xarr(3),garr(3)

gpole = droche(qmass, abcd(4), 0.0d0, abcd(3), rsep, frot)
gside = droche(qmass, abcd(4), abcd(2), 0.0d0, rsep, frot)
gback = droche(qmass, abcd(4)-abcd(1), 0.0d0, 0.0d0, rsep, frot)
gfront= droche(qmass, abcd(4)+abcd(1), 0.0d0, 0.0d0, rsep, frot)

if (verbose >= v_debug) then
  print *,' gmodel_coeff:  '
  print *,' abcd = ',abcd
  print *,' rsep = ',rsep
  print *,' frot = ',frot
  print *,' g_pole = ',gpole
  print *,' g_side = ',gside
  print *,' g_back = ',gback
  print *,' g_front= ',gfront
end if

xarr = [abcd(4)+abcd(1), abcd(4), abcd(4)-abcd(1)]
garr = [gfront/gpole-1.0d0,gside/gpole-1.0d0,gback/gpole-1.0d0]
ax = parfit(xarr,garr)
if (verbose >= v_debug) then
  print *,'xfit ',xarr
  print *,'gfit ',garr
  print *,'ax = ',ax
end if
gmodel(1:3) = ax

end function gmodel_coeffs
!-------------------------------------------------------------------------------
double precision function bright(f, g, npar, par, verbose)
!
!  Surface brightness at a point on an ellipsoidal star. 
!
!  To apply Doppler boosting set vscale to the rotation speed at the point
! (x,y,z) = (0,b,0) in km/s and set kboost to the Doppler boosting factor.
! 
!  To return the flux-weighted radial velocity set rvflag/=0 and vscale.
!
! For spherical stars only, sky-projected angle lambda between orbital and
! stellar rotation axes, can be non-zero.
!
! par(1) = Intensity at the centre of the stellar disc
! par(2) = a
! par(3) = b
! par(4) = c 
! par(5) = the
! par(6) = phi
! par(7) = rsep
! int(par(8)) = Limb darkening law
! par(9)  = Limb darkening coefficient 1
! par(10) = Limb darkening coefficient 2
! par(11) = Limb darkening coefficient 3
! par(12) = Limb darkening coefficient 4
!
! par(13:15) = Surface gravity model coefficients (if .not.exact_grav)
!              OR
! par(13) = q, mass ratio = mass of companion/mass of star (if exact_grav)
! par(14) = g0, local surface gravity at the pole (if exact_grav)
! par(15) = frot, asynchronous rotation factor
!
! par(16) = Gravity darkening coefficient (-v in Wood's notation)
! par(17) = Incident flux from companion
! par(18) = Heating/reflection model coefficient
! par(19) = Heating/reflection model exponent
! par(20) = Heating/reflection linear limb darkening coefficient
! par(21) = Companion radius/semi-major axis
! par(22) = lambda = sky-projected angle between orbital and rotation axes.
! par(23) = vscale = rotation speed at (x,y,z)=(0,b,0) in km/s
! par(24) = kboost = Doppler boosting factor
! par(25) = rvflag /= 0 to calculate flux-weighted radial velocity.
! par(26) = exact_grav /= 0 to use exact calculation of local surface gravity
! par(27-30) = Coordinate transformation 
!
! Coordinates
!  Position on the ellipse is "s" positive along the major axis of the star, 
! "t" parallel to orbital angular momentum vector.
! Position of companion is determined by sign of rsep, i.e., if rsep is
! positive then the companion is on the side of the star towards positive s.
!
! Position (s,t) on ellipse given by the following transformation of the
! input coordinates  (if npar >= 30)
! s = par(27) + par(29)*f + par(30)*g
! t = par(28) - par(30)*f + par(29)*g
! 
! **  If you use this transformation, remember to multiply the result of your
! integration by the Jacobian = par(29)**2 + par(30)**2
!
!
implicit none
integer, intent(in)  :: npar, verbose
double precision, intent(in) :: f,g,par(npar)

! Local variables
double precision :: I_0, F_0,s,t,a,b,c,the,phi,rsep,ldc(4)
double precision :: gmodel(3),vgrav,H_0,H_1,uheat,rcomp, q, g0, frot
double precision :: aw,bw,cw,dw
double precision, save :: costhe,sinthe,sinsqthe,sinsqphi,cossqthe,cossqphi
double precision, save :: sin2the,sin2phi,sinphi,cosphi
double precision, save :: phi_save = not_set_dble, the_save = not_set_dble
double precision :: w,x,y,z,s2,t2,st,a2,b2,c2,mu,lambda,rv,kboost
double precision :: ldfac,gfac,heat,radpt,r,rsq,cosgam,dcosgam, vscale
double precision, parameter :: c_kms = iau_c*1.0d-3 ! Speed of light in km/s
integer :: ldlaw
logical :: rvflag,exact_grav

I_0   = par(1)
a     = par(2) 
b     = par(3) 
c     = par(4) 
the   = par(5) 
phi   = par(6) 
rsep  = par(7) 
ldlaw = int(par(8))
ldc(1:4)    = par(9:12) 
vgrav  = par(16)
F_0    = par(17) 
H_0    = par(18)
H_1    = par(19)
uheat  = par(20)
rcomp  = par(21)
lambda = par(22)
vscale = par(23)
kboost = par(24)
rvflag = par(25).ne.0.0d0
exact_grav = par(26).ne.0.0d0
if (exact_grav) then
  q  = par(13) 
  g0 = par(14) 
  frot = par(15) 
else
  gmodel(1:3) = par(13:15)
end if
if (npar >= 30) then
  s = par(27) + par(29)*f + par(30)*g
  t = par(28) - par(30)*f + par(29)*g
else
  s = f
  t = g
end if

if ((vscale/=0.0d0).and.(lambda/=0.0d0).and.(abs(a-c)>epsilon(0.0d0))) then
  if(verbose >= v_error) then
    print *,'Error in bright - lambda /= 0 for non-spherical star.'
    print *,lambda,vscale
    print *,a,b,c,the,phi,s,t
  end if
  bright = bad_dble
  return
end if

! Dark star, no heating ...
heat = F_0*H_0
if ((I_0 == 0.0d0).and.(heat == 0.0d0)) then
  bright = 0
  return
end if

if (the /= the_save) then
  the_save = the
  costhe = cos(the)
  sinthe = sin(the)
  cossqthe = costhe**2
  sinsqthe = 1.d0-cossqthe
  sin2the = 2.d0*costhe*sinthe
end if
if (phi /= phi_save) then
  phi_save = phi
  cosphi = cos(phi)
  sinphi = sin(phi)
  cossqphi = cosphi**2
  sinsqphi = 1.d0-cossqphi
  sin2phi = 2.d0*cosphi*sinphi
end if


a2 = a**2
b2 = b**2
c2 = c**2
s2 = s**2
t2 = t**2
st = s*t

aw = sinsqthe*sinsqphi/a2 + sinsqthe*cossqphi/b2 + cossqthe/c2
bw = (sinthe*sin2phi*s - sin2the*sinsqphi*t)/a2   &
   - (sinthe*sin2phi*s + sin2the*cossqphi*t)/b2   &
   + sin2the*t/c2
cw = (cossqphi*s2 + cossqthe*sinsqphi*t2 - costhe*sin2phi*st)/a2 &
   + (sinsqphi*s2 + cossqthe*cossqphi*t2 + costhe*sin2phi*st)/b2 &
   + sinsqthe*t2/c2 - 1.d0
dw = bw**2 - 4.d0*aw*cw
if (dw < 0.d0) then
  ! The is usually a round-off error problem. If the radial distance of the
  ! point from the origin is within the minimum/maximum possible values then
  ! assume this is the case.
  if ((hypot(s,t) > c).and.(hypot(s,t) < a)) then
    bright = 0.0d0
    if(verbose >= v_debug) then
      print *,'bright: No such point on surface.'
      print *,hypot(s,t)-a,hypot(s,t)-b,hypot(s,t)-c
      print *,a,b,c,the,phi,dw
      print *,s,t,npar
      print *,f,g,par(27:30)
      print *,aw,bw,cw
    end if
    return
  else
    if(verbose > v_silent) then
      print *,'bright: No such point on surface.'
      print *,hypot(s,t)-a,hypot(s,t)-b,hypot(s,t)-c
      print *,a,b,c,the,phi,dw
      print *,s,t,npar
      print *,f,g,par(27:30)
      print *,aw,bw,cw
    end if
    bright = bad_dble
    return
  end if
end if

w = (-bw + sqrt(dw))/(2.d0*aw)
x = cosphi*s - costhe*sinphi*t + sinthe*sinphi*w
y = sinphi*s + costhe*cosphi*t - sinthe*cosphi*w
z =            sinthe*t        + costhe*w

! cosine of the angle between the line of sight and the surface normal to a
! triaxial ellipsoid.
mu = (x*sinphi*sinthe/a2 -y*sinthe*cosphi/b2 + z*costhe/c2) &
   /       sqrt(x*x/a2/a2 + y*y/b2/b2 + z*z/c2/c2)   
if ((mu <= 0.d0).or.(mu >= 1.d0)) then 
  print *,'Error in bright - mu out of range'
  print *,x,y,z,a2,b2,c2,sinthe,cosphi,mu
  bright = bad_dble
  return
end if

! Limb darkening
ldfac = limbdark(mu, ldlaw, ldc)
if (ldfac == bad_dble) then
  if(verbose >= v_error) then
    print *,'Error in bright - invalid parameters for limbdark.'
    print *,ldlaw,ldc
  end if
  bright = bad_dble
  return
end if

if (exact_grav) then
  gfac = (droche(q, x, y, z, abs(rsep), frot)/g0)**vgrav
else
  gfac =  (poly(gmodel(1:3),x)*(1.0d0-z**2/c2) + 1.0d0)**vgrav
end if

! Heating/reflection
if (heat /=  0.d0) then
  radpt   = sqrt(x**2 + y**2 + z**2)
  rsq =  radpt**2 - 2.d0*x*rsep + rsep**2
  r =  sqrt(rsq)
  cosgam = (x*rsep/radpt - radpt)/r
  dcosgam = (radpt-rcomp)/r
  if (cosgam < -dcosgam) then
    heat = 0
  else if (cosgam > dcosgam) then
    heat = heat*(1.0/rsq)**H_1*(1.d0-uheat*(1.d0-mu)) 
  else 
    heat = heat*(0.5d0*(cosgam+dcosgam)/dcosgam/rsq)**H_1*(1.d0-uheat*(1.d0-mu))
  end if
end if

bright = I_0*ldfac*gfac+heat
if (vscale /= 0.0d0) then
  if (lambda == 0.0d0) then
    rv = vscale*s/b
  else
    rv = vscale*(cos(lambda)*s - sin(lambda)*t)/b
  end if

  if (rvflag) then
    bright = rv*bright*(1.0d0 - kboost*rv/c_kms)
  else
    bright = bright*(1.0d0 - kboost*rv/c_kms)
  end if
else
  rv = 0
end if

if(verbose >= v_debug) then
  print *,'bright,s,t,rv,ldfac,gfac,heat= ',bright ,s,t,rv,ldfac,gfac,heat
end if

return

end function bright

!-------------------------------------------------------------------------------
double precision function eanom(m, e) 
!  Calculate the eccentric anomaly of a Keplerian orbit with
! eccentricity e, from the mean anomaly, m.
!
!  Solves Kepler''s equation using Newton-Raphson iteration using formula for
! initial estimate from Heintz DW, 'Double stars' (Reidel, 1978).
! 
!  Input:
!   m - Mean anomaly in radians.
!   e - Eccentrcity, 0 <= E < 1.
! 
!  Output:
!    Eccentric anomaly in the range 0 < eanom < 2*pi.
!    If e is out-of-range return bad_dble
!
implicit none
double precision,intent(in) :: m, e
integer, parameter  :: itmax = 9999
double precision, parameter :: etol=1.0d-9

! Local variables
double precision :: e0, e1, test
integer  :: it

if ( (e < 0.0d0).or.(e >= 1.0d0)) then
 print *, 'Invalid eccentricity value in function eanom'
 print *, e
 eanom = bad_dble
 return
endif

it = 0
e1 = mod(m,twopi) + e*sin(m) + e*e*sin(2.0d0*m)/2.0d0
test = 1.0d0
do while (test > etol)
 it = it + 1
 if (it .gt. itmax) then
  print *,'function eanom failed to converge'
  print *,m,e,e0,e1,test
  stop
 endif
 e0 = e1
 e1 = e0 + (m-(e0 - e*sin(e0)))/(1.0d0 - e*cos(e0))
 test = abs(e1 - e0)
end do
e1 = mod(e1, twopi)
if (e1 < 0.0d0) then
 e1 = e1 + twopi
endif 
eanom = e1
return
end function eanom

!-----------------------------------------------------------------------------

double precision function trueanom(m, e) 
!  Calculate the true anomaly of a Keplerian orbit with eccentricity e,
! from the mean anomaly, m.
!
! Uses: eanom
!
!  Input:
!   m - Mean anomaly in radians.
!   e - Eccentrcity, 0 <= e < 1.
!
! Output:
!   True anomaly in the range 0 to 2*PI.
!   If e is out-of-range return bad_dble
!  
implicit none
double precision,intent(in) :: m, e

! Local variables
double precision :: ee

if ( (e < 0.0d0).or.(e >= 1.0d0)) then
 print *, 'invalid eccentricity value in function trueanom'
 print *, e
 trueanom = bad_dble
 return
endif

ee = eanom(m,e)
trueanom = 2.0d0*atan(sqrt((1.0d0 + e)/(1.0d0 - e))*tan(ee/2.0d0))
return
end function trueanom

!-----------------------------------------------------------------------------

double precision function radvel(t, t0, p, v0, k, e, omrad) 
! Calculate radial velocity for a Keplerian orbit
!
! Uses: TRUEANOM
!
! Input:
!  T      - Time of observation
!  T0     - Time of periastron
!  P      - Orbital period
!  V0     - Systemic velocity
!  K      - Velocity semi-amplitude in the same units as V0
!  E      - Eccentricity of the orbit
!  OMRAD  - Longitude of periastron in radians.
!
!  Output:
!   Radial velocity in the same units as V0.
!
implicit none
double precision, intent(in) :: t, t0, p, v0, k, e, omrad

! Local variables
double precision :: m

m = twopi*mod((t-t0)/p,1.0d0)
if (e == 0.0d0) then
  radvel = v0 +k*cos(m+omrad)
  return
endif
if ( (e < 0.0d0).or.(e >= 1.0d0)) then
  print *, 'Invalid eccentricity value in function radvel'
  print *, e
  radvel = bad_dble
  return
endif

radvel = v0 + k*( e*cos(omrad) + cos(trueanom(m,e) + omrad))         
return
end function radvel

!------------------------------------------------------------------------------
double precision function t_ecl_to_peri(t_ecl, ecc, omega, incl, p_sid, verbose)
!
! Calculate the time of periastron passage immediately prior to a give time of
! eclipse. Equation numbers from Hilditch, "An Introduction to Close Binary
! Stars"
!
double precision, intent (in) :: t_ecl ! Time of eclipse
double precision, intent (in) :: ecc   ! Orbital eccentricity
double precision, intent (in) :: omega ! Longitude of periastron, radians
double precision, intent (in) :: incl  ! Orbital inclination, radians
double precision, intent (in) :: p_sid ! Siderial period
integer, intent (in) :: verbose
! Local variables
double precision :: theta, theta_0, delta_t, sin2i, efac, ee, eta, d
double precision, parameter :: tol = 1.0d-8
integer :: verbose1
integer, parameter :: npar = 4
double precision :: par(npar)

verbose1 = verbose_for_calls(verbose)
efac  = (1.0d0 - ecc**2)
sin2i = sin(incl)**2
! Value of theta for i=90 degrees
theta_0 = halfpi - omega ! True anomaly at superior conjunction
if (verbose >= v_debug) print *,'t_ecl_to_peri: theta_0 = ',theta_0
if (incl /= halfpi) then
 par = (/ efac, sin2i, omega, ecc /)
 d =  brent(theta_0-halfpi,theta_0,theta_0+halfpi, delta_func, npar, par, tol, &
            theta, verbose1)
else
  theta = theta_0
end if
if (verbose >= v_debug) print *,'t_ecl_to_peri: theta = ',theta

! (4.10)
if (theta == pi) then
  ee = pi
else
 ee = 2.0d0 * atan(sqrt((1.0d0-ecc)/(1.0d0+ecc)) * tan(theta/2.0d0))
end if
eta = ee - ecc*sin(ee)
delta_t = eta*p_sid/twopi
t_ecl_to_peri = t_ecl  - delta_t

end function t_ecl_to_peri

!------------------------------------------------------------------------------

double precision function delta_func(theta, npar, par, verbose)
implicit none
integer, intent(in)          :: npar, verbose
double precision, intent(in) :: theta, par(npar)
! Local variables
double precision :: efac, sin2i, omega, ecc

efac  = par(1)
sin2i = par(2)
omega = par(3)
ecc   = par(4)
delta_func = efac*sqrt(1.0d0 - sin2i*sin(theta+omega)**2)/(1.0d0+ecc*cos(theta))
end function delta_func

end module stellar
