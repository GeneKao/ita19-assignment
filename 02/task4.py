#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Task 4: traversing the mesh from boundary to boundary in a "straight" line.
"""

__author__ = "Gene Ting-Chun Kao"
__email__ = "kao@arch.ethz.ch"
__date__ = "30.10.2019"


def traverse_straight_line(mesh, vertex):
    """
    Traverse in mesh from boundary to boundary in a straight line.
    Args:
        mesh: compas.datastructure.Mesh, Mesh
        vertex: int, vertex key
    Returns:
        vertices: list of int, traverse path in vertex key
    """
    vertices = [vertex]

    while True:
        v = vertices.pop()

        if mesh.is_vertex_on_boundary(v) and len(vertices) > 0:
            break

        next_v = -1
        if len(vertices) == 0:
            for nbr in mesh.vertex_neighbors(v):
                if mesh.is_vertex_on_boundary(nbr):
                    continue
                next_v = nbr
                vertices.append(v)
        else:
            v2 = vertices.pop()
            face = mesh.halfedge[v2][v]
            next_v = mesh.face_vertex_descendant(face, v)

        vertices.append(next_v)
        face = mesh.halfedge[v][next_v]
        vertices.append(mesh.face_vertex_descendant(face, next_v))
        vertices.append(next_v)

    vertices.pop()
    print(vertices)

    return vertices


if __name__ == '__main__':
    import os
    import compas
    from compas.datastructures import Mesh
    from compas_plotters import MeshPlotter

    FILE = os.path.join(compas.DATA, 'faces.obj')
    mesh = Mesh.from_obj(FILE)

    vertices_path = traverse_straight_line(mesh, 1)

    plotter = MeshPlotter(mesh, figsize=(8, 5))

    plotter.draw_vertices(
        text={key: index for index, key in enumerate(mesh.vertex)},
        radius=0.3,
        facecolor={fkey: (255, 0, 0) for fkey in vertices_path})
    plotter.draw_edges()
    plotter.draw_faces()
    plotter.show()
