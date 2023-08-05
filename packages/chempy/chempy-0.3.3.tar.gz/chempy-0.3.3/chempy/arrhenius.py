# -*- coding: utf-8 -*-
"""
Contains functions for the `Arrhenius equation
<https://en.wikipedia.org/wiki/Arrhenius_equation>`_
(:func:`arrhenius_equation`) and a convenience fitting routine
(:func:`fit_arrhenius_equation`).
"""
from __future__ import (absolute_import, division, print_function)


def _get_R(constants=None, units=None):
    if constants is None:
        R = 8.314472
        if units is not None:
            J = units.Joule
            K = units.Kelvin
            mol = units.mol
            R *= J/mol/K
    else:
        R = constants.molar_gas_constant
    return R


def arrhenius_equation(A, Ea, T, constants=None, units=None, exp=None):
    """
    Returns the rate coefficient according to the Arrhenius equation

    Parameters
    ----------
    A: float with unit
        frequency factor
    Ea: float with unit
        activation energy
    T: float with unit
        temperature
    constants: object (optional, default: None)
        if None:
            T assumed to be in Kelvin, Ea in J/(K mol)
        else:
            attributes accessed: molar_gas_constant
            Tip: pass quantities.constants
    units: object (optional, default: None)
        attributes accessed: Joule, Kelvin and mol
    exp: callback (optional)
        callback for calculating the exponential, default: numpy.exp, math.exp

    """
    if exp is None:
        try:
            from numpy import exp
        except ImportError:
            from math import exp
    R = _get_R(constants, units)
    try:
        RT = (R*T).rescale(Ea.dimensionality)
    except AttributeError:
        RT = R*T
    return A*exp(-Ea/RT)


def fit_arrhenius_equation(k, T, kerr=None, linearized=False):
    """ Curve fitting of the Arrhenius equation to data points

    Parameters
    ----------
    k: array_like
    T: float
    kerr: array_like (optional)
    linearized: bool

    """

    if len(k) != len(T):
        raise ValueError("k and T needs to be of equal length.")
    from math import exp
    import numpy as np
    rT = 1/T
    lnk = np.log(k)
    p = np.polyfit(rT, lnk, 1)
    R = _get_R(constants=None, units=None)
    Ea = -R*p[0]
    A = exp(p[1])
    if linearized:
        return A, Ea
    from scipy.optimize import curve_fit
    if kerr is None:
        weights = None
    else:
        weights = 1/kerr**2
    popt, pcov = curve_fit(arrhenius_equation, T, k, [A, Ea], weights)
    return popt, pcov
