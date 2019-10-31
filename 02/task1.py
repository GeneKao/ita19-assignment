#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task 1: Given two vectors, use the cross product to create a set of three orthonormal vectors.
"""

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "29.10.2019"


def orthonormal_bases(u, v):
    """
    Generate three base vectors from two vectors
    Args:
        u: compas.geometry.Vector, first vector
        v: compas.geometry.Vector, second vector
    Returns:
        tuple of compas.geometry.Vector: three normalised vectors as list
    """
    return u.unitized(), u.cross(v).cross(u).unitized(), u.cross(v).unitized()


if __name__ == '__main__':

    from compas.geometry import Vector

    a = Vector(10, 10, 0)
    b = Vector(0, 10, 0)

    vectors = orthonormal_bases(a, b)
    print(vectors)
