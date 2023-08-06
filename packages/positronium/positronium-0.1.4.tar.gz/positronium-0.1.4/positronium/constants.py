#! python
'''
Physical constants
'''
from __future__ import print_function, division
from scipy.constants import m_e, e, c, h, hbar, alpha, Rydberg

# mass
m_Ps = 2.0 * m_e           # neglects binding energy
# reduced mass
reduced_mass_Ps = m_e/ 2.0
# Rydberg
Ryd_Ps = Rydberg / 2.0
Rydberg_Ps = Rydberg / 2.0
# Bohr radius
a_0 = hbar / (m_e * c * alpha)
# Ps Bohr raidus
a_Ps = 2.0 * a_0
# ground-state decay rate
decay_pPs = 7.9896178e9    # Phys. Rev. A 68 (2003) 032512
decay_oPs = 7.039968e6     # Phys. Rev. Lett. 85 (2000) 3065
# ground-state lifetime
tau_pPs = 1.0 / decay_pPs
tau_oPs = 1.0 / decay_oPs
# ground-state hyperfine splitting
nu_hfs = 2.033942e11       # Phys. Lett. B 734 (2014) 338
en_hfs = h * nu_hfs

## rescale atomic units
# energy
atomic_en = dict({'J': (lambda x: x * 2.0 * Rydberg * h * c),
                  'eV': (lambda x: x * 2.0 * Rydberg * h * c / e),
                  'meV': (lambda x: 1e3 * x * 2.0 * Rydberg * h * c / e),
                  'ueV': (lambda x: 1e6 * x * 2.0 * Rydberg * h * c / e),
                  'Hz': (lambda x: x * 2.0 * Rydberg * c),
                  'kHz': (lambda x: 1e-3 * x * 2.0 * Rydberg * c),
                  'MHz': (lambda x: 1e-6 * x * 2.0 * Rydberg * c),
                  'GHz': (lambda x: 1e-9 * x * 2.0 * Rydberg * c),
                  'THz': (lambda x: 1e-12 * x * 2.0 * Rydberg * c),
                  'm': (lambda x: 1.0 / (x * 2.0 * Rydberg)),
                  'cm': (lambda x: 1e2 / (x * 2.0 * Rydberg)),
                  'mm': (lambda x: 1e3 / (x * 2.0 * Rydberg)),
                  'um': (lambda x: 1e6 / (x * 2.0 * Rydberg)),
                  'nm': (lambda x: 1e9 / (x * 2.0 * Rydberg)),
                  'A': (lambda x: 1e10 / (x * 2.0 * Rydberg)),
                  'pm': (lambda x: 1e12 / (x * 2.0 * Rydberg)),
                  'fm': (lambda x: 1e15 / (x * 2.0 * Rydberg)),
                  'm^-1': (lambda x: x * 2.0 * Rydberg),
                  'cm^-1': (lambda x: 1e-2 * x * 2.0 * Rydberg)})
# distance
atomic_d = dict({'m': (lambda x: x * a_0),
                 'cm': (lambda x: x * a_0 * 1e2),
                 'mm': (lambda x: x * a_0 * 1e3),
                 'um': (lambda x: x * a_0 * 1e6),
                 'nm': (lambda x: x * a_0 * 1e9),
                 'A': (lambda x: x * a_0 * 1e10),
                 'pm': (lambda x: x * a_0 * 1e12),
                 'fm': (lambda x: x * a_0 * 1e15)})
