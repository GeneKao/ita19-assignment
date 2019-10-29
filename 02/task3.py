#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task 3: Define a function for computing the cross products of two arrays of vectors.
"""

import numpy as np

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "29.10.2019"


def cross_product_arrays(a, b):
    """
    Compute the cross products for two arrays of vectors using for loop
    Args:
        a: array of vectors: numpy.array, a list of vectors a
        b: array of vectors: numpy.array, a list of vectors b
    Returns:
        cross products: list of compas.geometry.Vector
    """
    if len(a) is not len(b):
        raise Exception("Input arrays need to be same length")

    return [Vector(*a[i]).cross(Vector(*b[i])) for i in range(len(a))]


def cross_product_numpy(a, b):
    """
    Compute the cross products for two arrays of vectors using numpy
    Args:
        a: array of vectors: numpy.array, a list of vectors a
        b: array of vectors: numpy.array, a list of vectors b
    Returns:
        cross products: array of vectors as list
    """
    if len(a) is not len(b):
        raise ValueError("Input arrays need to be same length")

    return np.cross(a, b)


if __name__ == '__main__':

    from random import randint
    from compas.geometry import Vector

    n = randint(2, 50)
    a = np.random.rand(n, 3)
    b = np.random.rand(n, 3)

    print(cross_product_arrays(a, b))
    print(cross_product_numpy(a,b))
    print(cross_product_numpy(a, b) == cross_product_arrays(a, b))
