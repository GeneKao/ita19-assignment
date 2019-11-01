import compas
from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector
from compas.geometry import normalize_vector
from compas.geometry import sum_vectors

import compas_rhino
from compas_rhino.artists import MeshArtist

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')
# numerical.stop_server()
# numerical.start_server()

# ==============================================================================
# Make a form finding mesh
# ==============================================================================

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.update_default_vertex_attributes({
    'px': 0.0,
    'py': 0.0,
    'pz': 0.0,
    'rx': 0.0,
    'ry': 0.0,
    'rz': 0.0,
    't': 0.1,
    'is_fixed': False})

mesh.update_default_edge_attributes({
    'q': 1.0,
    'f': 0.0,
    'l': 0.0})

# ==============================================================================
# Compute stuff
# ==============================================================================

# set the fixed vertices
# change the z value of the "high" vertices
# change the force density of the edges on the boundary
# compile the input for fd_numpy

for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue
    thickness = mesh.get_vertex_attribute(key, 't')

    # compute the vertex area
    # multiply by the local thickness
    # assign to the correct item in the list of loads

xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

# update the data structure

for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue

    # compute the load on the vertex
    # compute the forces in the edges connected to the vertex
    # sum up the vectors to compute the residual force

    resultant = sum_vectors(forces)
    mesh.set_vertex_attributes(key, ('rx', 'ry', 'rz'), resultant)

# ==============================================================================
# Visualise the result
# ==============================================================================

artist = MeshArtist(mesh, layer="Selfweight")
artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.draw_faces()

loads = []
for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue

    # append a dict to the list of loads
    # that will result in the drawing of a blue line
    # with an arrow at the end

compas_rhino.draw_lines(loads, layer=artist.layer, clear=False)

residuals = []
for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue

    # append a dict to the list of residuals
    # that will result in the drawing of a cyan line
    # with an arrow at the end

compas_rhino.draw_lines(residuals, layer=artist.layer, clear=False)
