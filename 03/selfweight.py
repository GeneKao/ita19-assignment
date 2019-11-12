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
corners = list(mesh.vertices_where({'vertex_degree': 2}))
mesh.set_vertices_attribute('is_fixed', True, keys=corners)
fixed = list(mesh.vertices_where({'is_fixed': True}))

# change the z value of the "high" vertices
high = [0, 35]
mesh.set_vertices_attribute('z', 7.0, keys=high)

# change the force density of the edges on the boundary
boundary = list(mesh.edges_on_boundary())
mesh.set_edges_attribute('q', 5.0, keys=boundary)

# compile the input for fd_numpy
xyz = mesh.get_vertices_attributes('xyz')
edges = list(mesh.edges())
q = mesh.get_edges_attribute('q')
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'))

for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue
    thickness = mesh.get_vertex_attribute(key, 't')

    # compute the vertex area
    area = mesh.vertex_area(key)
    # multiply by the local thickness
    weight = area * thickness
    # assign to the correct item in the list of loads
    loads[key][2] = -weight
    mesh.set_vertex_attributes(key, ('px', 'py', 'pz'), [0, 0, -weight])

xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

# update the data structure
for key, attr in mesh.vertices(True):
    attr['x'] = xyz[key][0]
    attr['y'] = xyz[key][1]
    attr['z'] = xyz[key][2]
    attr['rx'] = r[key][0]
    attr['ry'] = r[key][1]
    attr['rz'] = r[key][2]

for index, (u, v, attr) in enumerate(mesh.edges(True)):
    attr['f'] = f[index][0]

for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue

    # compute the load on the vertex
    load = loads[key]
    # compute the forces in the edges connected to the vertex
    forces = [load]
    for nbr in mesh.vertex_neighbors(key):
        # compute the force vector of the connected edge
        force = [a - b for a, b in zip(mesh.get_vertex_attributes(nbr, 'xyz'), mesh.get_vertex_attributes(key, "xyz"))]
        length = mesh.get_edge_attribute((key, nbr), 'f')
        print(length)
        force = scale_vector(normalize_vector(force), length)
        forces.append(force)

    # sum up the vectors to compute the residual force
    resultant = sum_vectors(forces)
    # print(resultant)
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
    load = mesh.get_vertex_attributes(key, ('px', 'py', 'pz'))
    # that will result in the drawing of a blue line
    vector = scale_vector(load, 1)
    start = mesh.vertex_coordinates(key)
    end = add_vectors(start, vector)
    # with an arrow at the end
    loads.append({
        'start': start,
        'end': end,
        'arrow': 'end',
        'color': (0, 0, 255)})

compas_rhino.draw_lines(loads, layer=artist.layer, clear=False)

residuals = []
for key in mesh.vertices():
    if mesh.get_vertex_attribute(key, 'is_fixed'):
        continue

    # append a dict to the list of residuals
    residual = mesh.get_vertex_attributes(key, ('rx', 'ry', 'rz'))
    # that will result in the drawing of a cyan line
    # with an arrow at the end
    vector = scale_vector(residual, 1)
    start = mesh.vertex_coordinates(key)
    end = add_vectors(start, vector)
    # with an arrow at the end
    residuals.append({
        'start': start,
        'end': end,
        'arrow': 'end',
        'color': (0, 255, 255)})


compas_rhino.draw_lines(residuals, layer=artist.layer, clear=False)
