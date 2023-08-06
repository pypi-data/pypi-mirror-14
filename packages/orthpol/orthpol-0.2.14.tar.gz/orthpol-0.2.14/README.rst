============
orthpol
============

This is the *orthpol* package. It is a frontend to the Fortran package orthpol written by W Gautschi [1].

[1] Gautschi, W. (1994). Algorithm 726: ORTHPOL–a package of routines for generating orthogonal polynomials and Gauss-type quadrature rules. ACM Transactions on Mathematical Software (TOMS), 20(1), 21–62. doi:10.1145/174603.174605

Status
======

`PyPi <https://pypi.python.org/pypi/orthpol/>`_:

.. image:: http://southpacific.no-ip.org:8080/buildStatus/icon?job=pypi-orthpol
   :target: http://southpacific.no-ip.org:8080/buildStatus/icon?job=pypi-orthpol

`LaunchPad <https://launchpad.net/pyorthpol>`_:

.. image:: http://southpacific.no-ip.org:8080/buildStatus/icon?job=orthpol
   :target: http://southpacific.no-ip.org:8080/buildStatus/icon?job=orthpol

`TestPyPi <https://testpypi.python.org/pypi/orthpol/>`_:

.. image:: http://southpacific.no-ip.org:8080/buildStatus/icon?job=testpypi-orthpol
   :target: http://southpacific.no-ip.org:8080/buildStatus/icon?job=testpypi-orthpol


Requirements
============

The package depends on a C++ porting of the Fortran library orthpol. Thus both C++ and Fortran compilers must be installed on the machine. The code is tested using the `GCC <https://gcc.gnu.org/>`_ compiler suite or `clang <http://clang.llvm.org/>`_ for the compilation and linking of C++ code, and the `gfortran <https://gcc.gnu.org/wiki/GFortran>`_ compiler for the Fortran part of the code.

Installation
============

Make sure to have an up-to-date version of pip:

    $ pip install --upgrade pip

Automatically install the software using the command:

    $ pip install orthpol

If this doesn't work, the package can be manually downloaded and installed through the following procedure:

   $ cd <download_dir>

   $ pip download orthpol

   $ tar xzf orthpol-X.X.X.tar.gz

   $ cd orthpol-X.X.X

   $ python setup.py install

Change Log
==========

0.1.0:
  * Initial python porting (working only for python 2.x)

0.2.0:
  * Modified interface to account for changes in the `SpectralToolbox <https://pypi.python.org/pypi/SpectralToolbox/>`_
  * Complete integration of orthpol into `SpectralToolbox <https://pypi.python.org/pypi/SpectralToolbox/>`_

0.2.1:
  * Porting to python 3.x and back compatibility with python 2.x
  * Automated installation through pip

0.2.2:
  * Bug fix

0.2.13:
  * Improved install script.

0.2.14:
  * Fixed bug in Py_polyeval. Access to data is now done only through PyArray_GETPTR macros.
