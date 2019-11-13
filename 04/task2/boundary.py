#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Texas Shell: Boundary structure
"""

from compas.datastructures import Mesh
from compas.geometry import add_vectors, scale_vector, cross_vectors, subtract_vectors
from compas.geometry import Frame, Point, Box
from compas.geometry import Transformation, transform_points
from compas.geometry import bounding_box_xy
from compas.geometry import offset_polygon
from compas.geometry import intersection_line_plane, distance_point_point
from compas.rpc import Proxy
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist, FrameArtist, PointArtist

import os

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "13.11.2019"


def draw(meshes):
    """Visualization"""

    # artist = FrameArtist(frame, layer="SOUTH::Frame", scale=0.3)
    # artist.draw()
    # artist = FrameArtist(frame_1, layer="SOUTH::Frame1", scale=0.3)
    # artist.draw()
    artist = MeshArtist(None, layer="SOUTH:Bboxes")
    artist.clear_layer()
    for mesh in meshes:
        artist.mesh = mesh
        # artist.clear_layer()
        artist.draw_mesh()


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

        if start > len(pts) - i -1:
            break

        count += 1
        if count >= 50:
            print('break---------!!!!')
            break

        points = pts[start:start+i+1]
        origin, axes, values = pca_numpy([list(point) for point in points])
        frame_1 = Frame(origin, axes[0], axes[1])
        X = Transformation.from_frame_to_frame(frame_1, Frame.worldXY())
        point2d = transform_points(points, X)
        bboxi = bounding_box_xy(point2d)
        bboxi = offset_polygon(bboxi, -PADDING)
        bboxi = transform_points(bboxi, X.inverse())

        if (distance_point_point(bboxi[0], bboxi[1]) > width_ub or
                distance_point_point(bboxi[1], bboxi[2]) > height_ub):

            bboxes.append(Mesh.from_vertices_and_faces(bbox, [[0, 1, 2, 3]]))
            start = start + i - 2
            i = 3
        elif i < len(pts) - start:
            bbox = bboxi
            i += 1
        else:
            continue

        print("len, ", len(bboxes))
        print("start, ", start)
        print('i-----, ', i)
        print('len pts, ', len(pts))

        print(start + i == len(pts))
        if start + i == len(pts):
            print("===============")
            bboxes.append(Mesh.from_vertices_and_faces(bboxi, [[0, 1, 2, 3]]))
            break

    return bboxes


if __name__ == '__main__':

    # Construct a cablenet
    HERE = os.path.dirname(__file__)
    FILE_I = os.path.join(HERE, 'cablenet.json')
    cablenet = Cablenet.from_json(FILE_I)

    # Parameters
    OFFSET = 0.200
    PADDING = 0.020

    # Vertices on SOUTH
    SOUTH = list(cablenet.vertices_where({'constraint': 'SOUTH'}))
    boundary = list(cablenet.vertices_on_boundary(ordered=True))
    SOUTH[:] = [key for key in boundary if key in SOUTH]

    # Boundary plane
    a = cablenet.vertex_coordinates(SOUTH[0])
    b = cablenet.vertex_coordinates(SOUTH[-1])

    xaxis = subtract_vectors(b, a)
    yaxis = [0, 0, 1.0]
    zaxis = cross_vectors(xaxis, yaxis)
    xaxis = cross_vectors(yaxis, zaxis)

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
    # PointArtist.draw_collection(intersections, layer="SOUTH:Intersections", clear=True)

    bboxes = pca_bboxes(intersections, 2.3, 0.2)
    draw(bboxes)