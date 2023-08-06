# positronium
python tools pertaining to positronium

## Prerequisites

Tested using Anaconda (Continuum Analytics) with Python 2.7 and 3.5.  Examples written using IPython 4.0.1 (python 3.5.1 kernel).

Package dependencies:

* scipy

IPython examples dependencies:

* numpy
* matplotlib

## Installation

via pip (recommended):

```
pip install positronium
```

alternatively, try the development version

```
git clone https://github.com/PositroniumSpectroscopy/positronium
```

and then run

```
python setup.py install
```

### Disclaimer
This package is very much under development: module / functions/ variables names, functionality,
etc. are all subject to change. 

## About

This package is designed to collate useful bits of code relating to the positronium atom
(an electron bound to its antiparticle, the positron).

The package currently only contains two very simple modules.

*constants* is intended to collect useful constants.  For example,

```python
>>> from positronium.constants import tau_oPs, nu_hfs
>>> print("The mean lifetime of ortho-Ps is", "%.1f ns."%(tau_oPs * 1e9))
The mean lifetime of ortho-Ps is 142.0 ns.

>>> print("The ground-state hyperfine splitting is", "%.1f GHz."%(nu_hfs * 1e-9))
The ground-state hyperfine splitting is 203.4 GHz.
```

*Bohr* uses an adaption of the Rydberg formula (sim. to hydrogen) to calculate the principle
energy levels of positronium, or the interval between two levels.  The default unit is 'eV',
however, this can be changed using the keyword argument 'unit'.

For instance, the UV wavelength (in nm) needed to excite the Lyman-alpha transition can be found by:

```python
>>> from positronium import Bohr
>>> Bohr.energy(1, 2, unit='nm')
243.00454681357735
```

For further examples see the IPython/ Jupter notebooks,

https://github.com/PositroniumSpectroscopy/positronium/tree/master/examples
