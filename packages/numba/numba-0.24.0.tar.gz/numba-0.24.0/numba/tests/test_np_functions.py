# Tests numpy methods of <class 'function'>
from __future__ import print_function, absolute_import, division

import itertools
import math
import sys

import numpy as np

from numba import unittest_support as unittest
from numba.compiler import compile_isolated, Flags, utils
from numba import typeof, types
from .support import TestCase, CompilationCache

no_pyobj_flags = Flags()
no_pyobj_flags.set("nrt")


def sinc(x):
    return np.sinc(x)

def angle1(x):
    return np.angle(x)

def angle2(x, deg):
    return np.angle(x, deg)


class TestNPFunctions(TestCase):
    """
    Contains tests and test helpers for numpy methods the are of type
    "class< 'function' >.
    """

    def setUp(self):
        self.ccache = CompilationCache()

    def run_unary(self, pyfunc, x_types, x_values, flags=no_pyobj_flags,
                  func_extra_types=None, func_extra_args=None,
                  ignore_sign_on_zero=False, abs_tol=None, **kwargs):
        """
        Runs tests for a unary function operating in the numerical real space.

        Parameters
        ----------
        pyfunc : a python function definition holding that calls the numpy
                 functions to be tested.
        x_types: the types of the values being tested, see numba.types
        x_values: the numerical values of the values to be tested
        flags: flags to pass to the CompilationCache::ccache::compile function
        func_extra_types: the types of additional arguments to the numpy
                          function
        func_extra_args:  additional arguments to the numpy function
        ignore_sign_on_zero: boolean as to whether to allow zero values
        with incorrect signs to be considered equal
        prec: the required precision match, see assertPreciseEqual

        Notes:
        ------
        x_types and x_values must have the same length

        """
        for tx, vx in zip(x_types, x_values):
            if func_extra_args is None:
                func_extra_types = func_extra_args = [()]
            for xtypes, xargs in zip(func_extra_types, func_extra_args):
                cr = self.ccache.compile(pyfunc, (tx,) + xtypes,
                                         flags=flags)
                cfunc = cr.entry_point
                got = cfunc(vx, *xargs)
                expected = pyfunc(vx, *xargs)
                try:
                    scalty = tx.dtype
                except AttributeError:
                    scalty = tx
                prec = ('single'
                        if scalty in (types.float32, types.complex64)
                        else 'double')
                msg = 'for input %r with prec %r' % (vx, prec)
                self.assertPreciseEqual(got, expected,
                                        prec=prec,
                                        msg=msg,
                                        ignore_sign_on_zero=
                                        ignore_sign_on_zero,
                                        abs_tol=abs_tol, **kwargs)

    def test_sinc(self):
        """
        Tests the sinc() function.
        This test is purely to assert numerical computations are correct.
        """

        # Ignore sign of zeros, this will need masking depending on numpy
        # version once the fix to numpy complex division is in upstream
        # See: https://github.com/numpy/numpy/pull/6699
        isoz = True

        # Testing sinc(1.) leads to sin(pi)/pi, which is below machine
        # precision in practice on most machines. Small floating point
        # differences in sin() etc. may lead to large differences in the result
        # that are at a range that is inaccessible using standard width
        # floating point representations.
        # e.g. Assume float64 type.
        # sin(pi) ~= 1e-16, but should be zero
        # sin(pi)/pi ~= 1e-17, should be zero, error carried from above
        # float64 has log10(2^53)~=15.9 digits of precision and the magnitude
        # change in the alg is > 16  digits (1.0...0 -> 0.0...0),
        # so comparison via ULP is invalid.
        # We therefore opt to assume that values under machine precision are
        # equal in this case.
        tol = "eps"

        pyfunc = sinc

        def check(x_types, x_values, **kwargs):
            self.run_unary(pyfunc, x_types, x_values,
                                ignore_sign_on_zero=isoz, abs_tol=tol,
                                **kwargs)

        # real domain scalar context
        x_values = [1., -1., 0.0, -0.0, 0.5, -0.5, 5, -5, 5e-21, -5e-21]
        x_types = [types.float32, types.float64] * (len(x_values) // 2)
        check(x_types, x_values)

        # real domain vector context
        x_values = [np.array(x_values, dtype=np.float64)]
        x_types = [typeof(v) for v in x_values]
        check(x_types, x_values)

        # complex domain scalar context
        x_values = [1.+0j, -1+0j, 0.0+0.0j, -0.0+0.0j, 0+1j, 0-1j, 0.5+0.0j,
                    -0.5+0.0j, 0.5+0.5j, -0.5-0.5j, 5+5j, -5-5j,
                    # the following are to test sin(x)/x for small x
                    5e-21+0j, -5e-21+0j, 5e-21j, +(0-5e-21j)
                    ]
        x_types = [types.complex64, types.complex128] * (len(x_values) // 2)
        check(x_types, x_values, ulps=2)

        # complex domain vector context
        x_values = [np.array(x_values, dtype=np.complex128)]
        x_types = [typeof(v) for v in x_values]
        check(x_types, x_values, ulps=2)


    def test_angle(self, flags=no_pyobj_flags):
        """
        Tests the angle() function.
        This test is purely to assert numerical computations are correct.
        """
        pyfunc1 = angle1
        pyfunc2 = angle2

        def check(x_types, x_values):
            # angle(x)
            self.run_unary(pyfunc1, x_types, x_values)
            # angle(x, deg)
            xtra_values = [(True,), (False,)]
            xtra_types = [(types.bool_,)] * len(xtra_values)
            self.run_unary(pyfunc2, x_types, x_values,
                           func_extra_types=xtra_types,
                           func_extra_args=xtra_values,)

        # real domain scalar context
        x_values = [1., -1., 0.0, -0.0, 0.5, -0.5, 5, -5]
        x_types = [types.float32, types.float64] * (len(x_values) // 2 + 1)
        check(x_types, x_values)

        # real domain vector context
        x_values = [np.array(x_values, dtype=np.float64)]
        x_types = [typeof(v) for v in x_values]
        check(x_types, x_values)

        # complex domain scalar context
        x_values = [1.+0j, -1+0j, 0.0+0.0j, -0.0+0.0j, 1j, -1j, 0.5+0.0j,
                    -0.5+0.0j, 0.5+0.5j, -0.5-0.5j, 5+5j, -5-5j]
        x_types = [types.complex64, types.complex128] * (len(x_values) // 2 + 1)
        check(x_types, x_values)

        # complex domain vector context
        x_values = np.array(x_values)
        x_types = [types.complex64, types.complex128]
        check(x_types, x_values)
