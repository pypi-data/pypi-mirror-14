#! python
"""
Created on Sat Feb 27 11:35:54 2016

@author: Adam
"""
from __future__ import print_function, division
import numpy as np
import positronium.constants as constants

def field(n, unit='V cm^-1'):
    '''
    For each value of n the ionization field for the outermost Stark state with
    a negative Stark shift is approximately equal to the classical ionization
    field.

    T. F. Gallagher, Rydberg Atoms (Cambridge University Press, Cambridge,
    England, 1994).

    kwargs:
        unit:
            V m^-1, V cm^-1      [electric field]

    defaults:
        n = 1
        unit='V cm^-1'
    '''
    rescale = {'V m^-1': (lambda x: x),
               'V cm^-1': (lambda x: 0.01 * x)}
    if unit not in rescale:
        raise KeyError('"' + unit + '" is not recognised as a suitable unit. See' +
                       ' docstring for unit list.')
    efield = np.reciprocal(np.power(n, 4.0)) * 2.0 * constants.Ryd_Ps * \
                           constants.h * constants.c / (constants.e * constants.a_Ps * 9.0)
    return rescale[unit](efield)
