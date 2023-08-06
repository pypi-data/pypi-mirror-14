'''Helper module in popmodel containing constants and functions for OH
calculations.
'''

## Literature cited:

# Bradshaw et al, Appl Opt, 23, 2134 (1984)
# Daily et al., Applied Optics 16 (3), 568-571 (1977)
# Fuchs et al., Atmos Meas Tech, 1611-1626(2012)
# Schlosser et al., J Atmos Chem, 56, 187-205 (2007)
# Tsuji et al, Bull Chem Soc Jpn, 73, 2695-2702 (2000)
# van de Meerakker et al, Phys Rev Lett, 95, 013003 (2005)

from __future__ import division
from . import atmcalcs as atm

import math as m
import numpy as np
from scipy.constants import k as kb
from scipy.constants import c, N_A, pi, h
import scipy.special

#######################

def kqavg(kn2, ko2, kh2o, xh2o=0.02):
    '''get average k in air (default 0.78 N2/0.20 O2/0.02 H2O)'''
    xn2 = 0.79-xh2o/2
    xo2 = 0.21-xh2o/2
    return xn2*kn2 + xo2*ko2 + xh2o*kh2o

#######################

### Literature values for OH
MASS = 17.01/(N_A)*1000    # kg

NU12 = 3407.53 * atm.WAVENUM_TO_HZ  # Hz, IR transition used in Tsuji et al,
# 2000. Illustrative example; popmodel extracts precise wavenumber for given IR
#       transition from HITRAN.

## Degeneracies
# Generally, degeneracies for rotational quantum number J are 2J+1. The ground
# electronic state is PI, so lambda doubling doubles the degeneracies. A-state
# is SIGMA, so there is no lambda doubling.

# Example values for 3-level system where IR transition is P branch and UV is
# Q branch:
GA = 20    # (J = 4.5)
GB = 16    # (J = 3.5)
GC = 8    # From (2*J + 1) and N = 3 (?) for Tsuji et al. feature. Assuming
            # Q branch.

## Einstein coefficients
# Aba is very slow and unimportant for popmodel calculations.
ABA = 16.9      # Einstein coefficient for spontaneous emission, s^-1;
                # using van de Meerakker et al, 2005
                # alt value: 14.176 s^-1 from Tsuji et al, 2000

# Einstein coefficients for A--X transitions, Copeland et al. 1987 Chem Phys
# Lett 138, 425-430. ADICT not directly accessed in main.KineticsRun code
# (instead looks at rates in parameter yaml file) but is kept here as
# reference.
ADICT = {'00': 1.44e6, '01': 5.3e3, '10': 5.11e5, '11': 8.38e5}

## Rotational relaxation
# Define in terms of depopulation rate of rotational level of interest. Model
# also needs to include repopulation rate such that thermal distribution is
# reached at equilibrium.
RROUT = np.array([7.72e-10, 7.72e-10, 4.65e-10])
# Smith and Crosley, 1990 model rates. Undifferentiated by quencher or v.

## Lambda doublet relaxation
LROUT = 4.5e-10 # ballpark placeholder

## Thermal rotational distribution
# Use LIFBASE-calculated thermal distributions at 296 K for both halves of each
# lambda doublet -- can later divide in half to calculate population in each
# half of lambda doublet (equal e and f).
# X(v"=0) rotational levels
# F1 term (PI_3/2) where J = N + 0.5 (starts with N=1)
ROTFRAC_A1 = np.array([[0.1147102,
                        0.1373055,
                        0.1333955,
                        0.1108903,
                        0.0807381,
                        0.0521280,
                        0.0300671,
                        0.0155687]])
# F2 term (PI_1/2) where J = N - 0.5 (starts with N=1)
ROTFRAC_A2 = np.array([[0.0303408,
                        0.0520817,
                        0.0605903,
                        0.0566615,
                        0.0449620,
                        0.0310304,
                        0.0188811,
                        0.0102155]])
# X(v"=1) rotational levels
# F1 term
ROTFRAC_B1 = np.array([[0.1118301,
                        0.1346591,
                        0.1319314,
                        0.1108789,
                        0.0818258,
                        0.0536861,
                        0.0315495,
                        0.0166880]])
# F2 term
ROTFRAC_B2 = np.array([[0.0295226,
                        0.0509050,
                        0.0596629,
                        0.0563731,
                        0.0453257,
                        0.0317841,
                        0.0197044,
                        0.0108914]])
# to avoid digging into mess of calculating populations for A_SIGMA just assume
# distribution is more or less like X(v"=0). Tenuous connection to reality.
ROTFRAC_C = ROTFRAC_A1+ROTFRAC_A2
ROTFRAC_D = ROTFRAC_C
# build rotfrac dict for extraction in main.py
ROTFRAC = {}
ROTFRAC['a'] = np.concatenate((ROTFRAC_A1, ROTFRAC_A2))
ROTFRAC['b'] = np.concatenate((ROTFRAC_B1, ROTFRAC_B2))
ROTFRAC['c'] = ROTFRAC_C[0]
ROTFRAC['d'] = ROTFRAC_D[0]

## HITRAN data for 3407 cm^-1 IR transition
# v = 0 --> v = 1, J = 4.5 --> J = 3.5
# loadHITRAN automates extracting these values from arbitrary IR OH line

G_AIR = .053    # air-broadened HWHM, cm^-1 atm^-1 at 296K

G_SELF = .03    # self-broadened HWHM, cm^-1 atm^-1 at 296K

N_AIR = .66    # coeff of temp dependence of air-broadened half-width

# uncertainties in HITRAN data for this transition:
# in wavenumber: 3 ('0.001 - 0.01')
# in intensity: 4 ('10-20%')
# in g-air: 2 ('avg or estimate')
# in g-self: 0 ('unreported')
# in n_air: 1 ('default')
# in air-pressure shift: 0 ('unreported') -- value given as 0

### Laser operating parameters
# No longer call these particular values in popmodel KineticsRun calcs. Do use
# spec_intensity function, though.
TEMP = 296.    # temperature, K. All HITRAN data assumes 296K!

BEAM_DIAM_IR = 5e-3    # beam diameter, m

BEAM_DIAM_UV = 5e-3    # beam diameter, m

BANDWIDTH_IR = 1e6    # Hz, Aculight spec
BANDWIDTH_UV = 7e9    # Hz, Schlosser et al 2007.

POWER_IR = 3    # W, Aculight spec
POWER_UV = 50e-3    # W, Schlosser et al 2007, average power

REPRATE_UV = 8.5e3    # Hz, Fuchs et al. 2012
PERIOD_UV = 1/REPRATE_UV    # s
PULSEWIDTH_UV = 30e-9    #s, somewhat arbitrary, Fuchs et al. report 25 ns pulse

def peakpower(avgpower, pulsewidth, reprate):
    '''Calculate peak power for a pulsed laser given average power, laser
    period, and pulse width.'''
    if pulsewidth is not None and reprate is not None:
        return avgpower/(pulsewidth*reprate)
    else:
        raise ValueError('require non-None pulsewidth and reprate values for ',
                         'peakpower calc')

PEAK_POWER_UV = peakpower(POWER_UV, PULSEWIDTH_UV, REPRATE_UV) # W, peak power

# Beam parameters
A_IR = pi*(.5*BEAM_DIAM_IR)**2 # beam area, m^2
A_UV = pi*(.5*BEAM_DIAM_UV)**2

# Spectral radiances (intensities) for master equations, W/m^2*sr*Hz
# Note IR is CW laser, while UV is pulsed.
def spec_intensity(power, area, bandwidth):
    '''Caclulate spectral intensity (W/(m^2*Hz)) given power, area, bandwidth.
    '''
    return power/(area*bandwidth)

LAB = spec_intensity(POWER_IR, A_IR, BANDWIDTH_IR)
LBC = spec_intensity(PEAK_POWER_UV, A_UV, BANDWIDTH_UV)

OP_PRESS = 2. # operating pressure of detection cell, torr
              # Julich LIF instrument operates at
              # 3.5 hPa = 2.6 torr (Fuchs et al.)
              # 8.5 hPa = 6.4 torr (Schlosser et al.)
XOH = 0.5e-12 # 0.5 pptv, ballpark (1.2E7 cm^-3 at 760 torr, 296 K)

# Quenching:
XH2O = 0.02    # mole fraction of water
Q = atm.press_to_numdens(OP_PRESS, TEMP) # total 'quencher' conc, molec/cm^3

# Quenching speciated by N2/O2/H2O: (s^-1/(molec cm^-3))
# Full result of lit search in 'vib excited lifetime calcs OH TP LIF.xlsx'.
# Define estimated rate constants based on these values.
KQBH2O = 1.36e-11 # Reported value for multiple groups, +/-0.4e-11; however,
                # Silvente et al. give value 50% larger
KQBO2 = 1e-13 # Choose intermediate value between reported measurements of
            # 7.5e-14 and 1.3e13
KQBN2 = 1.5e-15 # Only one reported measurement (D'Ottone et al.), but this term
              # is a minor contribution
KQB = kqavg(KQBN2, KQBO2, KQBH2O, XH2O)

QUENCHB = KQB * Q # s^-1

# Electronic quenching of A state (s^-1/(molec cm^-3))
KQCH2O = 68.0e-11 # Wysong et al. 1990, v'=0
KQCO2 = 13.5e-11 # Wysong et al. 1990, v'=0
KQCN2 = 1.9e-11 # Copeland et al. 1985, v'=0, N'=3 (other N available -- gets
                # smaller with bigger N)
KQC = kqavg(KQCN2, KQCO2, KQCH2O, XH2O)

QUENCHC = KQC * Q # s^-1

###############################

## Functions for calculations

# N.B. Two conventions for Einstein B coefficient:
# (1) Spectral radiance (intensity)
# Spectral intensity L is laser power per (area, solid angle and frequency)
# L: J m^-2 s^-1 Hz^-1 sr^-1 = W m^-2 Hz^-1 sr^-1
#     units of B: m^2 J^-1 s^-1 = s kg^-1
# (2) Energy density rho: J m^-3 Hz^-1 sr^-1 = W s m^-3 Hz^-1 sr^-1
#     units of B: m^3 J^-1 s^-2 = m kg^-1
# We're using (1), intensity convention, e.g., Daily et al., 1977.
# L and rho are related by L = c*rho (see McQuarrie Ch. 15).
# L and rho are also per solid angle, or sr^-1 -- see Wikipedia.

def b21(a21, freq):
    '''
    Calculate Einstein coefficient for stimulated emission from A
    coefficient, using McQuarrie Eqn 15.13 and dividing by c to
    convert to intensity convention, m^2 J^-1 s^-1.

    Also consistent with Demtroder 3rd ed, assuming typo in eqn. 2.22.
    (i.e., missing nu^3 in numerator, h is to first power)
    Provides result consistent with Frank's value of 1e8 for OH
    excitation to v' = 1 from email 16 May 2014.

    Parameters
    ----------
    a21 : float (or 1D numpy array)
    Einstein A coefficient for spontaneous emission, s^-1.
    freq : float (or 1D numpy array)
    Frequency of transition, Hz.

    Returns
    -------
    b21_coeff : float (or 1D numpy array)
    Einstein B coefficient for stimulated emission, m^2 J^-1 s^-1.
    '''
    b21_coeff = a21 * c**2 / (8. * m.pi * h * freq**3)
    return b21_coeff

def b12(a21, g_lower, g_upper, freq):
    '''
    Calculate Einstein coefficient for absorption from A coefficient.

    Parameters
    ----------
    a21: float (or 1D numpy array)
    Einstein A coefficient for spontaneous emission, s^-1.
    g_lower, g_upper: float (or 1D numpy array)
    Degeneracies of lower and upper states. Function converts g's to float
    to avoid high likelihood of int division.
    freq : float (or 1D numpy array)
    Frequency of transition, Hz.

    Returns
    -------
    b12 : float (or 1D numpy array)
    Einstein B coefficient for absorption, m^2 J^-1 s^-1.
    '''
    b12_coeff = (np.array(g_upper).astype(float)/
                 np.array(g_lower).astype(float) *
                 b21(a21, freq))
    return b12_coeff

def fwhm_doppler(nu, temp, mass):
    '''
    Calculates FWHM, Hz, of peak from Doppler broadening.

    Source: Demtroder 3rd ed., p 70 (Eqn 3.43a)
    '''
    fwhm = (2*m.pi*nu/c) * (8*kb*temp*m.log(2)/mass)**0.5
    return fwhm

def calculateuv(N_upper, vib_upper, f_upper, E_lower):
    '''
    Calculate uv transition wavenumber, accounting for rotational states.

    Looks up sigma-state energy level in v'=0 or v'=1 with rotational level
    N from 0 to 29.

    PARAMETERS:
    -----------
    N_upper : int
    N quantum number for upper state.

    vib_upper : int
    Vibrational level of upper state (0 or 1)

    f_upper : int
    F number of upper state (1 or 2)

    E_lower : float
    Energy of lower state, cm^-1.

    OUTPUTS:
    --------
    wnum_uv : float
    Wavenumber of UV transition, cm^-1.
    '''
    # use Table 11 of Dieke and Crosswhite (JQSRT 1962) for sigma-state energy
    # levels (source for A(v'=0) energies from McGee and McIlrath 1984 paper
    # previously used here -- should be consistent with previous calcs if they
    # were correctly performed with accurate UV transition choice)
    if vib_upper == 0:
        if f_upper == 1:
            # v'=0, F1
            energylist = [32440.61,
                          32474.62,
                          32542.56,
                          32644.22,
                          32779.49,
                          32948.31,
                          33150.14,
                          33384.97,
                          33652.29,
                          33951.80,
                          34282.99,
                          34645.53,
                          35038.61,
                          35462.01,
                          35914.82,
                          36396.66,
                          36906.50,
                          37443.91,
                          38007.90,
                          38597.79,
                          39212.69,
                          39851.66,
                          40513.79,
                          41198.19,
                          41903.78,
                          42629.60,
                          43374.41,
                          44137.43,
                          44917.20,
                          45712.85]
        elif f_upper == 2:
            # v'=0, F2
            energylist = [32440.50,
                          32474.30,
                          32541.98,
                          32643.45,
                          32778.49,
                          32947.05,
                          33148.73,
                          33383.26,
                          33650.38,
                          33949.67,
                          34280.64,
                          34642.92,
                          35035.86,
                          35459.02,
                          35911.59,
                          36393.24,
                          36902.90,
                          37440.15,
                          38003.93,
                          38593.62,
                          39208.99,
                          39847.20,
                          40509.23,
                          41193.51,
                          41898.86,
                          42624.65,
                          43369.31,
                          44132.26,
                          44911.77,
                          45707.33]
        else:
            raise ValueError("invalid f_upper: ", f_upper)
    elif vib_upper == 1:
        if f_upper == 1:
            # v'=1, F1
            energylist = [35429.16,
                          35461.50,
                          35526.06,
                          35622.71,
                          35751.30,
                          35911.70,
                          36103.59,
                          36326.71,
                          36580.68,
                          36865.21,
                          37179.72,
                          37523.85,
                          37897.08,
                          38298.85,
                          38728.43,
                          39185.24,
                          39668.56,
                          40177.74,
                          40711.81,
                          41270.16,
                          41851.78,
                          42455.86,
                          43081.34,
                          43727.39,
                          44392.89,
                          45076.75,
                          45777.83,
                          46495.18,
                          47227.29,
                          47973.14]
        elif f_upper == '2':
            # v'=1, F2
            energylist = [35429.06,
                          35461.18,
                          35525.52,
                          35621.95,
                          35750.32,
                          35910.50,
                          36102.19,
                          36325.11,
                          36578.88,
                          36863.21,
                          37177.52,
                          37521.45,
                          37894.49,
                          38296.05,
                          38725.43,
                          39182.09,
                          39665.20,
                          40174.24,
                          40708.09,
                          41266.28,
                          41847.68,
                          42451.64,
                          43076.97,
                          43722.90,
                          44388.16,
                          45072.13,
                          45773.00,
                          46490.18,
                          47222.07,
                          47967.87]
        else:
            raise ValueError("invalid f_upper: ", f_upper)
    else:
        raise ValueError("invalid vib_upper: ", vib_upper)
    E_upper = energylist[N_upper]
    wnum_uv = E_upper - E_lower
    return wnum_uv

def press_broaden(press=OP_PRESS):
    '''
    Uses HITRAN parameters to calculate HWHM, in MHz, at 'press' in torr.
    '''
    hwhm = press * atm.TORR_TO_ATM * (G_AIR) * atm.WAVENUM_TO_HZ / 1e6
    return hwhm

def sat(bandwidth, beam, q=QUENCHB, freq=NU12, a21=ABA):
    '''
    Calculates power when saturation parameter equals 1, following Daily et
    al., 1977, i.e., when population of excited state is half of ground state,
    scaled by degeneracies. Full saturation is when parameter is >>1.

    Parameters
    ----------
    bandwidth : float
    Bandwidth of laser, MHz
    beam : float
    Beam diameter, mm
    q : float
    combined quenching and spontaneous emission rate (Q + A), s^-1.
    Default value is literature OH v"=1 --> v"=0 quench rate.
    freq : float
    Frequency of transition, Hz
    a21 : float
    Einstein A coefficient for spontaneous emission, s^-1.

    Returns
    -------
    sat_power : float
    Power when saturation parameter is 1, W.
    '''

    sat_intensity = q / b21(a21, freq)
    beam_area = m.pi * (0.5 * beam / 1.e3)**2
    # power is I * A * bandwidth
    sat_power = sat_intensity * beam_area * (bandwidth * 1.e6)

    return sat_power

def voigt(xarr, amp, xcen, sigma, gamma, normalized=False):
    '''Normalized Voigt profile from pyspeckit, on Github.

    z = (x+i*gam)/(sig*sqrt(2))
    V(x,sig,gam) = Re(w(z))/(sig*sqrt(2*pi))

    The area of V in this definition is 1.
    If normalized=False, then you can divide the integral of V by
    sigma*sqrt(2*pi) to get the area.

    Original implementation converted from
    http://mail.scipy.org/pipermail/scipy-user/2011-January/028327.html
    (had an incorrect normalization and strange treatment of the input
    parameters)

    Modified implementation taken from wikipedia, using the definition.
    http://en.wikipedia.org/wiki/Voigt_profile

    Parameters
    ----------
    xarr : np.ndarray
    The X values over which to compute the Voigt profile
    amp : float
    Amplitude of the voigt profile
    if normalized = True, amp is the AREA
    xcen : float
    The X-offset of the profile
    sigma : float
    The width / sigma parameter of the Gaussian distribution -- standard
    deviation
    gamma : float
    The width / shape parameter of the Lorentzian distribution -- HWHM
    normalized : bool
    Determines whether "amp" refers to the area or the peak of the voigt
    profile

    Outputs
    -------
    V : np.ndarray
    Voigt profile y values for xarr, either normalized or not.
    '''
    z = ((xarr-xcen) + 1j*gamma) / (sigma * np.sqrt(2))
    V = amp * np.real(scipy.special.wofz(z))
    if normalized:
        return V / (sigma*np.sqrt(2*np.pi))
    else:
        return V
