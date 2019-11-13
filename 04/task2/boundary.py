#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Texas Shell: Boundary structure
"""

from compas.datastructures import Mesh
from compas.geometry import add_vectors, scale_vector, cross_vectors, subtract_vectors
from compas.geometry import Frame, Point, Vector
from compas.geometry import Transformation, transform_points
from compas.geometry import bounding_box_xy
from compas.geometry import offset_polygon
from compas.geometry import intersection_line_plane, distance_point_point
from compas.rpc import Proxy
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist

import os

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "13.11.2019"


def pca_bboxes(pts, width_ub, height_ub):
    """create a pca bounding boxes from points"""

    # Create a proxy for PCA
    numerical = Proxy('compas.numerical')
    pca_numpy = numerical.pca_numpy

    bboxes = []
    start = 0
    bbox = None
    count = 0
    i = 3
    print(len(pts))
    while True:

        if start > len(pts) - i - 1:
            break

        count += 1
        if count >= 50:
            break

        points = pts[start: start + i + 1]
        origin, axes, values = pca_numpy([list(point) for point in points])
        frame_1 = Frame(origin, axes[0], axes[1])
        X = Transformation.from_frame_to_frame(frame_1, Frame.worldXY())
        point2d = transform_points(points, X)
        bboxi = bounding_box_xy(point2d)
        bboxi = offset_polygon(bboxi, -PADDING)
        bboxi = transform_points(bboxi, X.inverse())

        if (distance_point_point(bboxi[0], bboxi[1]) > width_ub or
                distance_point_point(bboxi[1], bboxi[2]) > height_ub):

            bboxes.append(bbox_extrude(bbox))

            start = start + i - 1
            i = 3
        elif i < len(pts) - start:
            bbox = bboxi
            i += 1
        else:
            continue

        if start + i == len(pts):
            bboxes.append(bbox_extrude(bboxi))
            break

    return bboxes


def bbox_extrude(bbox, dist=0.05):
    """draw a extruded bbox"""

    top = []
    normal = scale_vector(Vector(*cross_vectors(subtract_vectors(bbox[0], bbox[1]),
                           subtract_vectors(bbox[0], bbox[3]))).unitized(), dist)
    for a in bbox:
        b = add_vectors(a, normal)
        top.append(b)
    vertices = bbox + top
    faces = [[0, 3, 2, 1], [4, 5, 6, 7], [3, 0, 4, 7], [2, 3, 7, 6], [1, 2, 6, 5], [0, 1, 5, 4]]

    return Mesh.from_vertices_and_faces(vertices, faces)


def get_intersection(side):
    # Vertices on SOUTH
    SOUTH = list(cablenet.vertices_where({'constraint': side}))
    boundary = list(cablenet.vertices_on_boundary(ordered=True))
    SOUTH[:] = [key for key in boundary if key in SOUTH]

    # Boundary plane
    a = cablenet.vertex_coordinates(SOUTH[0])
    b = cablenet.vertex_coordinates(SOUTH[-1])
    c = cablenet.vertex_coordinates(SOUTH[1])

    if side == 'SOUTH' or side == 'NORTH':
        xaxis = subtract_vectors(b, a)
        yaxis = subtract_vectors(c, a)
    else:
        xaxis = subtract_vectors(c, a)
        yaxis = subtract_vectors(b, a)
    zaxis = cross_vectors(xaxis, yaxis)
    xaxis = cross_vectors(yaxis, zaxis)
    # the bbox direction is not clear. so to specifically extrude in one direction,
    # need more implementation later.

    frame = Frame(a, xaxis, yaxis)
    point = add_vectors(frame.point, scale_vector(frame.zaxis, OFFSET))
    normal = frame.zaxis
    plane = point, normal

    # Intersections
    intersections = []
    for key in SOUTH:
        a = cablenet.vertex_coordinates(key)
        r = cablenet.residual(key)
        b = add_vectors(a, r)
        x = intersection_line_plane((a, b), plane)
        intersections.append(Point(*x))

    return intersections


if __name__ == '__main__':

    # Construct a cablenet
    HERE = os.path.dirname(__file__)
    FILE_I = os.path.join(HERE, 'cablenet.json')
    cablenet = Cablenet.from_json(FILE_I)

    # Parameters
    OFFSET = 0.200
    PADDING = 0.020

    sides = ['NORTH', 'SOUTH', 'WEST', 'EAST']

    artist = MeshArtist(None, layer="SOUTH:Bboxes")
    artist.clear_layer()

    for side in sides:
        intersections = get_intersection(side)

        # my algorithm has a problem, the width_ub, height_ub need to be tweaked.
        # since bbox only make box when there's more than 3 points.
        # the method  need to be improved later when I have time.
        bboxes = pca_bboxes(intersections, 1.4, 0.46)

        for mesh in bboxes:
            artist.mesh = mesh
            artist.draw_faces(join_faces=True, color=(0, 255, 255))