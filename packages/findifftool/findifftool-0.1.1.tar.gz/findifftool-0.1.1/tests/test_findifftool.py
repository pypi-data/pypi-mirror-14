#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_findifftool
----------------------------------

Tests for `findifftool` module.
"""

import unittest
import numpy
from . import findifftool

from findifftool.core import *
from findifftool.attributes import *


class TestFindifftool(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_scalar_gradient(self):
        def f(x):
            return x**2
        self.assertAlmostEqual(grad(f)(3), 6)

    def test_scalar_hessian(self):
        def f(x):
            return x**3
        self.assertAlmostEqual(hessian(f)(3), 18, delta=10*DELTA)

    def test_2d_gradient(self):
        def f(x, y):
            return x**2 + y**2
        gradf = grad(f)
        numpy.testing.assert_allclose(gradf(3, 4), (6, 8))

    def test_2d_hessian(self):
        def f(x, y):
            return x**2 + y**2
        hessf = hessian(f)
        numpy.testing.assert_allclose(hessf(3, 4), (2, 0, 2), rtol=10*DELTA)

    def test_2_array_gradient(self):
        def f(x_arr):
            return numpy.dot(x_arr, x_arr)
        x = numpy.array((3., 4.))
        numpy.testing.assert_allclose(ndgrad(f)(x), (6, 8))

    def test_2_array_hessian(self):
        def f(x_arr):
            return numpy.dot(x_arr, x_arr)
        x = numpy.array((3., 4.))
        numpy.testing.assert_allclose(ndhess(f)(x), ((2, 0),(0, 2)), rtol=10*DELTA, atol=10*DELTA)

    def test_2_matrix_gradient(self):
        def f(x):
            return x[0, 0]**2 + x[1, 1]**2 - x[0, 1]*x[1, 0]
        x = numpy.array([[1., 2.], [3., 4.]])
        numpy.testing.assert_allclose(ndgrad(f)(x), [[2, -3], [-2, 8]])

    def test_2_matrix_hessian(self):
        def f(x):
            return x[0, 0]**2 + x[1, 1]**2 - x[0, 1]*x[1, 0]
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([2, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 2]).reshape((2,2,2,2))
        numpy.testing.assert_allclose(ndhess(f)(x), ref_hess, rtol=10*DELTA, atol=10*DELTA)

    def test_diff_class_method_gradient(self):
        class A(object):
            def __init__(self, data):
                self.x = data

            def exe(self):
                return self.x[0, 0]**2 + self.x[1, 1]**2 - self.x[0, 1]*self.x[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        a_instance = A(x)
        numpy.testing.assert_allclose(clgrad(a_instance, 'exe', 'x')(), [[2, -3], [-2, 8]])

    def test_diff_class_method_hessian(self):
        class A(object):
            def __init__(self, data):
                self.x = data

            def exe(self):
                return self.x[0, 0]**2 + self.x[1, 1]**2 - self.x[0, 1]*self.x[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([2, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 2]).reshape((2,2,2,2))
        a_instance = A(x)
        numpy.testing.assert_allclose(clhess(a_instance, 'exe', 'x')(), ref_hess, rtol=10*DELTA, atol=10*DELTA)

    def test_diff_class_method_gradient_with_args(self):
        class A(object):
            def __init__(self, data):
                self.x = data

            def exe(self, dummy):
                return self.x[0, 0]**2 + self.x[1, 1]**2 - self.x[0, 1]*self.x[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        a_instance = A(x)
        numpy.testing.assert_allclose(clgrad(a_instance, 'exe', 'x')(None), [[2, -3], [-2, 8]])

    def test_diff_class_method_hessian_with_args(self):
        class A(object):
            def __init__(self, data):
                self.x = data

            def exe(self, dummy):
                return self.x[0, 0]**2 + self.x[1, 1]**2 - self.x[0, 1]*self.x[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([2, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 2]).reshape((2,2,2,2))
        a_instance = A(x)
        numpy.testing.assert_allclose(clhess(a_instance, 'exe', 'x')(None), ref_hess, rtol=10*DELTA, atol=10*DELTA)

    def test_diff_class_method_gradient_with_kwargs(self):
        class A(object):
            def __init__(self, data):
                self.x = data

            def exe(self, dummy=None):
                return self.x[0, 0]**2 + self.x[1, 1]**2 - self.x[0, 1]*self.x[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        a_instance = A(x)
        numpy.testing.assert_allclose(clgrad(a_instance, 'exe', 'x')(None), [[2, -3], [-2, 8]])

    def test_diff_class_method_hessian_with_kwargs(self):
        class A(object):
            def __init__(self, data):
                self.x = data

            def exe(self, dummy=None):
                return self.x[0, 0]**2 + self.x[1, 1]**2 - self.x[0, 1]*self.x[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([2, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 2]).reshape((2,2,2,2))
        a_instance = A(x)
        numpy.testing.assert_allclose(
            clhess(a_instance, 'exe', 'x')(None), ref_hess, rtol=10*DELTA, atol=10*DELTA
            )

    def test_diff_class_method_gradient_unique(self):
        class A(object):
            def __init__(self, data):
                self.x = data
                self.y = data

            def exe(self, dummy=None):
                return self.x[0, 0]*self.y[0, 0] + self.x[1, 1]*self.y[1, 1] - self.x[0, 1]*self.y[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        a_instance = A(x)
        numpy.testing.assert_allclose(clgrad(a_instance, 'exe', 'y')(None), [[1, 0], [-2, 4]])

    def test_diff_class_method_hessian_unique(self):
        class A(object):
            def __init__(self, data):
                self.x = data
                self.y = data

            def exe(self, dummy=None):
                return self.x[0, 0]*self.y[0, 0] + self.x[1, 1]*self.y[1, 1] - self.x[0, 1]*self.y[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape((2,2,2,2))
        a_instance = A(x)
        numpy.testing.assert_allclose(
            clhess(a_instance, 'exe', 'x')(None), ref_hess, rtol=10*DELTA, atol=10*DELTA
            )

    def test_diff_class_method_hessian_mixed(self):
        class A(object):
            def __init__(self, data):
                self.x = data
                self.y = data

            def exe(self, dummy=None):
                return self.x[0, 0]*self.y[0, 0] + self.x[1, 1]*self.y[1, 1] - self.x[0, 1]*self.y[1, 0]

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape((2,2,2,2))
        a_instance = A(x)
        numpy.testing.assert_allclose(
            clmixhess(a_instance, 'exe', 'x', 'y')(None), ref_hess, rtol=10*DELTA, atol=10*DELTA
            )

    def test_diff_class_submethod_gradient(self):
        class A(object):
            def __init__(self, data):
                self.x = data
                self.y = data

            def exe(self, dummy=None):
                return self.x[0, 0]*self.y[0, 0] + self.x[1, 1]*self.y[1, 1] - self.x[0, 1]*self.y[1, 0]


        class B(object):
            def __init__(self, data):
                self.a = A(data)

                
        x = numpy.array([[1., 2.], [3., 4.]])
        b_instance = B(x)
        numpy.testing.assert_allclose(clgrad(b_instance, 'a.exe', 'a.y')(None), [[1, 0], [-2, 4]])

    def test_diff_class_submethod_hessian(self):
        class A(object):
            def __init__(self, data):
                self.x = data
                self.y = data

            def exe(self, dummy=None):
                return self.x[0, 0]*self.y[0, 0] + self.x[1, 1]*self.y[1, 1] - self.x[0, 1]*self.y[1, 0]


        class B(object):
            def __init__(self, data):
                self.a = A(data)

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).reshape((2,2,2,2))
        b_instance = B(x)
        numpy.testing.assert_allclose(
            clhess(b_instance, 'a.exe', 'a.y')(None), ref_hess, rtol=10*DELTA, atol=10*DELTA
            )

    def test_diff_class_submethod_mixed_hessian(self):
        class A(object):
            def __init__(self, data):
                self.x = data
                self.y = data

            def exe(self, dummy=None):
                return self.x[0, 0]*self.y[0, 0] + self.x[1, 1]*self.y[1, 1] - self.x[0, 1]*self.y[1, 0]


        class B(object):
            def __init__(self, data):
                self.a = A(data)

                
        x = numpy.array([[1., 2.], [3., 4.]])
        ref_hess = numpy.array([1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape((2,2,2,2))
        b_instance = B(x)
        numpy.testing.assert_allclose(clmixhess(
            b_instance, 'a.exe', 'a.x', 'a.y')(None), ref_hess, rtol=10*DELTA, atol=10*DELTA
            )

    def test_CTC(self):


        class Nod(object):
            #
            #
            # Class global variables
            #
            S = numpy.array([[1., .1], [.1, 1.]])
            C = numpy.array([[.7, .6], [.6, -.7]])

            def __init__(self, astring, bstring, C=None, tmpdir='/tmp'):
                #
                # Input: list of orbital indices for alpha and beta strings
                #
                self.a = astring
                self.b = bstring

            def __mul__(self, other):
                #
                # Return overlap of two Slater determinants <K|L>
                # calculated as matrix determinant of overlap
                # of orbitals in determinants
                # det(S) = det S(alpha)*det S(beta)
                #
                #
                if len(self.a) != len(other.a) or len(self.b) != len(other.b):
                    return 0

                (CKa, CKb) = self.orbitals()
                (CLa, CLb) = other.orbitals()
                #
                # alpha
                #
                Det = 1
                if CKa is not None:
                    SKLa = numpy.dot(CKa.T, numpy.dot(Nod.S, CLa))
                    Deta = numpy.linalg.det(SKLa)
                    Det *= Deta
                #
                # beta
                #
                if CKb is not None:
                    SKLb = numpy.dot(CKb.T, numpy.dot(Nod.S, CLb))
                    Detb = numpy.linalg.det(SKLb)
                    Det *= Detb
                #
                return Det

            def orbitals(self):
                CUa = None
                CUb = None
                if self.a: CUa = self.C[:, self.a]
                if self.b: CUb = self.C[:, self.b]
                return (CUa, CUb)


        class NodPair(object):
            """Non-orthogonal determinant pairs"""

            def __init__(self, K, L):
                self.K = K
                self.L = L

            def __str__(self):
                return "<%s|...|%s>" % (self.K, self.L)

            def overlap(self):
                return self.K*self.L

            def right_orbital_gradient(self):
                """Rhs derivative <K|dL/dC(mu, m)>"""
                DmoKL = Dmo(self.K, self.L)
                CK = self.K.orbitals()

                KdL = full.matrix(Nod.C.shape)
                if self.K(0):
                    KdLa = Nod.S*CK[0]*DmoKL[0]*self.overlap()
                    KdLa.scatteradd(KdL, columns=self.L(0))
                if self.K(1):
                    KdLb = Nod.S*CK[1]*DmoKL[1]*self.overlap()
                    KdLb.scatteradd(KdL, columns=self.L(1))
                
                return KdL

        KL = NodPair(Nod([0], [0]), Nod([0], [0]))

        numpy.testing.assert_allclose(clgrad(KL, 'overlap', 'L.C')(), [[1.41968, 0.0], [1.25156, 0.0]])
        reset_attribute(KL, 'L.C')
        #
        # This illustrates that when <K| and |L> are the same object, replacing L.C with a copy will
        # do the same for |K> and the numerical difference will be on the whole. How to fix?
        # Somehow replace KL.L with a copy
        #
        a0b0 = Nod([0], [0])
        KL = NodPair(a0b0, a0b0)
        numpy.testing.assert_allclose(clgrad(KL, 'overlap', 'L.C')()/2, [[1.41968, 0.0], [1.25156, 0.0]])
            
        

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
