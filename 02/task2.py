#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task2: Use the cross product to compute the area of a convex, 2D polygon.
"""

from compas.utilities import pairwise

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "29.10.2019"


def convex_polygon_area(polygon):
    """
    Calculate area from polygon
    Args:
        polygon: compas.geometry, convex polygon
    Returns:
        float: area of the convex polygon
    """
    # check if the polygon is convex
    if not polygon.is_convex():
        raise ValueError("Please give a convex polygon")

    pts = polygon.points[:] + [polygon.points[0]]
    # calculate all triangle areas using polygon centroid
    areas = [area_from_3_pts(a, b, polygon.centroid) for a, b in pairwise(pts)]

    return sum(areas)


def area_from_3_pts(a, b, c):
    """
    Compute the area from three points
    Args:
        a: compas.geometry.Point, pt1
        b: compas.geometry.Point, pt2
        c: compas.geometry.Point, pt3
    Returns:
        float: are of three points
    """
    return 0.5 * (b - a).cross(c - a).length


if __name__ == '__main__':

    from compas.geometry import Polygon

    polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [-0.5, 0.5, 0]])
    area = convex_polygon_area(polygon)

    print("Polygon area is: ", area, "\nIs my result same as compas result: ", area == polygon.area)
