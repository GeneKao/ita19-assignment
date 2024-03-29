import os
from compas_fofin.datastructures import Cablenet
from compas_rhino.artists import MeshArtist
from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import offset_polygon
from compas.geometry import intersection_line_plane
from compas.utilities import pairwise
import json

# ==============================================================================
# Set the path to the input file.
# The input file was generated with `FOFIN_to`, which serialises the cablenet
# data structure to JSON.
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'cablenet.json')
FILE_O = os.path.join(HERE, 'blocks.json')

# ==============================================================================
# Make a cablenet.
# ==============================================================================

cablenet = Cablenet.from_json(FILE_I)

# ==============================================================================
# Flip the cycles of the mesh because the cycles are currently such that the
# normals point to the interior of the structure.
# Note that you could also just flip the cycles once and update the JSON file.
# ==============================================================================

mesh_flip_cycles(cablenet)

# ==============================================================================
# Set the value of the thickness of the foam blocks in [m].
# Set the value of the offset distance for the edges of the faces to create space
# for the ribs.
# ==============================================================================

THICKNESS = 0.060
OFFSET = 0.020

# ==============================================================================
# Generate the formwork blocks.
# ==============================================================================

blocks = []

for fkey in cablenet.faces():
    
    vertices = cablenet.face_vertices(fkey)
    points = cablenet.get_vertices_attributes('xyz', keys=vertices)

    # the edges of the bottom face polygon have to be offset to create space
    # for the ribs.

    bottom = offset_polygon(points[:], OFFSET)

    # the vertices of the top face are the intersection points of the face normal
    # placed at each (offset) bottom vertex and a plane perpendicular to the 
    # face normal placed at a distance THICKNESS along the face normal from the
    # face centroid.

    # define the plane
    origin = cablenet.face_centroid(fkey)
    normal = cablenet.face_normal(fkey, unitized=True)
    plane = add_vectors(origin, scale_vector(normal, THICKNESS)), normal

    top = []
    for a in bottom:
        b = add_vectors(a, normal)
        xyz = intersection_line_plane((a, b), plane)
        top.append(xyz)

    top[:] = offset_polygon(top, OFFSET)

    vertices = bottom + top
    faces = [[0, 3, 2, 1], [4, 5, 6, 7], [3, 0, 4, 7], [2, 3, 7, 6], [1, 2, 6, 5], [0, 1, 5, 4]]

    block = Mesh.from_vertices_and_faces(vertices, faces)

    blocks.append(block)

# ==============================================================================
# Visualize the block with a mesh artist in the specified layer. Use
# `draw_faces` (with `join_faces=True`) instead of `draw_mesh` to get a flat
# shaded result. Also draw the vertex labels tovisualize the cycle directions.
# ==============================================================================

artist = MeshArtist(None, layer="FOFIN:Blocks")
artist.clear_layer()

# overwrite the output json file
open(FILE_O, 'w').close()

for mesh in blocks:
    artist.mesh = mesh
    artist.draw_faces(join_faces=True, color=(0, 255, 255))
    artist.draw_vertexlabels()

    # Serialise the meshes into a json file. each block start from a new line.
    with open(FILE_O, 'a+') as fp:
        json.dump(mesh.data, fp)
        fp.write('\n')


