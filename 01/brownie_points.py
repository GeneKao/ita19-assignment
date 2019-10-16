#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is my solution for the extra brownie points
"""

from random import random

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "16.10.2019"


def cross_product_3d(a, b):
    """
        Generate arbitrary vectors from arbitrary plane defined by P and normal
        Args:
            a: tuple, 3d vector
            b: tuple, 3d vector
        Returns:
            a cross product vector as a tuple
    """
    return a[1]*b[2] - a[2]*b[1], a[0]*b[2] - a[2]*b[0], a[0]*b[1] - a[1]*b[0]


def random_vec_on_plane(P, normal):
    """
    Generate arbitrary vectors from arbitrary plane defined by P and normal
    Args:
        P: tuple, point
        normal: tuple, vector
    Returns:
        a random vector as tuple
    """

    # Basically for doing this just generate a random vector
    # and do the cross_product with normal then it will be on the plane.
    vec = (random(), random(), random())
    return cross_product_3d(normal, vec)


if __name__ == '__main__':
    # test with points.txt to see if the result is correct using compas
    from compas.geometry import Plane, Point
    from task2 import read_pt_from_txt

    points = read_pt_from_txt('points.txt')
    for pt3 in points:
        pts = [Point(*p) for p in pt3]
        pl = Plane.from_three_points(*pts)
        print(pl)
        vec = random_vec_on_plane(pl.point, pl.normal)

        # check if the vector end point is on the plane
        vec_end = (pl.point[0]+vec[0], pl.point[1]+vec[1], pl.point[2]+vec[2])
        p = Point(*vec_end)
        print(p.distance_to_plane(pl))





