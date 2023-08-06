# -*- coding: utf-8 -*-
"""
General finite difference utlity for generation of finite difference first
and second derivative functions given a scalar input function


Functions:

    grad: for ordinary scalar functions of one or two variables
    ndgrad: for scalar functions of numpy array objects
    clgrad: for derivatives of a class method with respect to an attribute
"""

import numpy
from .attributes import get_method_and_copy_of_attribute
DELTA = 5e-5

def grad(f, delta=DELTA):
    """
    Returns numerical gradient function of given input function
    Input: f, scalar function of one or two variables
           delta(optional), finite difference step
    Output: gradient function object
    """
    def grad_f(*args, **kwargs):
        if len(args) == 1:
            x, = args
            gradf_x = (
                f(x+delta/2) - f(x-delta/2)
                )/delta
            return gradf_x
        elif len(args) == 2:
            x, y = args
            if type(x) in [float, int] and type(y) in [float, int]:
                gradf_x = (f(x + delta/2, y) - f(x - delta/2, y))/delta
                gradf_y = (f(x, y + delta/2) - f(x, y - delta/2))/delta
                return gradf_x, gradf_y
    return grad_f

def hessian(f, delta=DELTA):
    """
    Returns numerical hessian function of given input function
    Input: f, scalar function of one or two variables
           delta(optional), finite difference step
    Output: hessian function object
    """
    def hessian_f(*args, **kwargs):
        if len(args) == 1:
            x, = args
            hessianf_x = (
                f(x+delta) + f(x-delta) - 2*f(x)
                )/delta**2
            return hessianf_x
        elif len(args) == 2:
            x, y = args
            if type(x) in [float, int] and type(y) in [float, int]:
                hess_xx = (
                    f(x + delta, y) + f(x - delta, y) - 2*f(x, y)
                    )/delta**2
                hess_yy = (
                    f(x, y + delta) + f(x, y - delta) - 2*f(x, y)
                    )/delta**2
                hess_xy = (
                    + f(x+delta/2, y+delta/2)
                    + f(x-delta/2, y-delta/2)
                    - f(x+delta/2, y-delta/2)
                    - f(x-delta/2, y+delta/2)
                    )/delta**2
                return hess_xx, hess_xy, hess_yy
    return hessian_f

def ndgrad(f, delta=DELTA):
    """
    Returns numerical gradient function of given input function
    Input: f, scalar function of an numpy array object
           delta(optional), finite difference step
    Output: gradient function object
    """
    def grad_f(*args, **kwargs):
        x = args[0]
        grad_val = numpy.zeros(x.shape)
        it = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
        for xi in it:
            i = it.multi_index
            xi += delta/2
            fp = f(*args, **kwargs)
            xi -= delta
            fm = f(*args, **kwargs)
            xi += delta/2
            grad_val[i] = (fp - fm)/delta
        return grad_val
    return grad_f

def ndhess(f, delta=DELTA):
    """
    Returns numerical hessian function of given input function
    Input: f, scalar function of an numpy array object
           delta(optional), finite difference step
    Output: hessian function object
    """
    def hess_f(*args, **kwargs):
        x = args[0]
        hess_val = numpy.zeros(x.shape + x.shape)
        it = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
        for xi in it:
            i = it.multi_index
            jt = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
            for xj in jt:
                j = jt.multi_index
                xi += delta/2
                xj += delta/2
                fpp = f(x)
                xj -= delta
                fpm = f(x)
                xi -= delta
                fmm = f(x)
                xj += delta
                fmp = f(x)
                xi += delta/2
                xj -= delta/2
                hess_val[i + j] = (fpp + fmm - fpm - fmp)/delta**2
        return hess_val
    return hess_f

def clgrad(obj, exe, arg, delta=DELTA):
    """
    Returns numerical gradient function of given class method
    with respect to a class attribute
    Input: obj, general object
           exe (str), name of object method
           arg (str), name of object atribute
           delta(float, optional), finite difference step
    Output: gradient function object
    """
    f, x = get_method_and_copy_of_attribute(obj, exe, arg)
    def grad_f(*args, **kwargs):
        grad_val = numpy.zeros(x.shape)
        it = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
        for xi in it:
            i = it.multi_index
            xi += delta/2
            fp = f(*args, **kwargs)
            xi -= delta
            fm = f(*args, **kwargs)
            xi += delta/2
            grad_val[i] = (fp - fm)/delta
        return grad_val
    return grad_f

def clhess(obj, exe, arg, delta=DELTA):
    """
    Returns numerical hessian function of given class method
    with respect to a class attribute
    Input: obj, general object
           exe (str), name of object method
           arg (str), name of object atribute
           delta(float, optional), finite difference step
    Output: Hessian function object
    """
    f, x = get_method_and_copy_of_attribute(obj, exe, arg)
    def hess_f(*args, **kwargs):
        hess_val = numpy.zeros(x.shape + x.shape)
        it = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
        for xi in it:
            i = it.multi_index
            jt = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
            for xj in jt:
                j = jt.multi_index
                xi += delta/2
                xj += delta/2
                fpp = f(*args, **kwargs)
                xj -= delta
                fpm = f(*args, **kwargs)
                xi -= delta
                fmm = f(*args, **kwargs)
                xj += delta
                fmp = f(*args, **kwargs)
                xi += delta/2
                xj -= delta/2
                hess_val[i + j] = (fpp + fmm - fpm - fmp)/delta**2
        return hess_val
    return hess_f

def clmixhess(obj, exe, arg1, arg2, delta=DELTA):
    """
    Returns numerical mixed Hessian function of given class method
    with respect to two class attributes
    Input: obj, general object
           exe (str), name of object method
           arg1(str), name of object attribute
           arg2(str), name of object attribute
           delta(float, optional), finite difference step
    Output: Hessian function object
    """
    f, x = get_method_and_copy_of_attribute(obj, exe, arg1)
    _, y = get_method_and_copy_of_attribute(obj, exe, arg2)
    def hess_f(*args, **kwargs):
        hess_val = numpy.zeros(x.shape + y.shape)
        it = numpy.nditer(x, op_flags=['readwrite'], flags=['multi_index'])
        for xi in it:
            i = it.multi_index
            jt = numpy.nditer(y, op_flags=['readwrite'], flags=['multi_index'])
            for yj in jt:
                j = jt.multi_index
                xi += delta/2
                yj += delta/2
                fpp = f(*args, **kwargs)
                yj -= delta
                fpm = f(*args, **kwargs)
                xi -= delta
                fmm = f(*args, **kwargs)
                yj += delta
                fmp = f(*args, **kwargs)
                xi += delta/2
                yj -= delta/2
                hess_val[i + j] = (fpp + fmm - fpm - fmp)/delta**2
        return hess_val
    return hess_f
