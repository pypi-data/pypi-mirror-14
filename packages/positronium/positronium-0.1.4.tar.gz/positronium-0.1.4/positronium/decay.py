#! python
"""
Created on Sat Feb 27 11:35:54 2016

@author: Adam
"""
from __future__ import print_function, division
import numpy as np
import positronium.constants as constants

TAU_0 = 3.0*constants.hbar / (2.0 * constants.alpha**5.0 * \
                            constants.reduced_mass_Ps * constants.c**2.0)

def radiative(n, l=0, unit='s'):
    '''
    A universal formula for the radiative mean lifetime of hydrogenlike states (n,l).
    The formula is accurate to at least 6% for the lowest states and to a much higher
    degree of accuracy for highly excited states.

        Semiclassical estimation of the radiative mean lifetimes of hydrogenlike states
        Hermann Marxer and Larry Spruch
        Phys. Rev. A 43, 1268
        https://dx.doi.org/10.1103/PhysRevA.43.1268

    kwargs:
        unit:
            s, ms, us, ns, ps,                      [lifetime]
            Hz, kHz, MHz, GHz, THz, PHz, EHz,       [rate]

    defaults:
        n = 1
        l = 0
        unit='s'
    '''
    rescale = {'s': (lambda x: x),
               'ms': (lambda x: x*1e3),
               'us': (lambda x: x*1e6),
               'ns': (lambda x: x*1e9),
               'ps': (lambda x: x*1e12),
               'Hz': (lambda x: 1.0/ x),
               'kHz': (lambda x: 1.0/ x * 1e-3),
               'MHz': (lambda x: 1.0/ x * 1e-6),
               'GHz': (lambda x: 1.0/ x * 1e-9),
               'THz': (lambda x: 1.0/ x * 1e-12),
               'PHz': (lambda x: 1.0/ x * 1e-15),
               'EHz': (lambda x: 1.0/ x * 1e-18)}
    if unit not in rescale:
        raise KeyError('"' + unit + '" is not recognised as a suitable unit. See' +
                       ' docstring for unit list.')
    lifetime = TAU_0 * np.multiply(np.power(n, 3.0), np.multiply(l, np.add(l, 1)))
    return rescale[unit](lifetime)
