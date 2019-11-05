import compas
from compas.datastructures import Mesh

from compas_rhino.selectors import EdgeSelector
from compas_rhino.modifiers import EdgeModifier
from shell import Shell
from shellartist import ShellArtist

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')
# numerical.stop_server()
# numerical.start_server()

# ==============================================================================
# Make a form finding mesh
# ==============================================================================



shell = Shell.from_obj(compas.get('faces.obj'))

# ==============================================================================
# Compute stuff
# ==============================================================================

# set the fixed vertices
corners = list(shell.vertices_where({'vertex_degree': 2}))
shell.set_vertices_attribute('is_fixed', True, keys=corners)
fixed = list(shell.vertices_where({'is_fixed': True}))

# change the z value of the "high" vertices
high = [0, 35]
shell.set_vertices_attribute('z', 7.0, keys=high)

# change the force density of the edges on the boundary
boundary = list(shell.edges_on_boundary())
shell.set_edges_attribute('q', 5.0, keys=boundary)

shell.fofin()

# ==============================================================================
# Visualization helpers
# ==============================================================================

artist = ShellArtist(shell, layer="Selfweight")
artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.draw_faces()
artist.redraw()

def redraw():
    artist.clear_layer()
    artist.draw_vertices()
    artist.draw_edges()
    artist.draw_faces()
    artist.redraw()

# ==============================================================================
# Edges attributes
# ==============================================================================
while True:
    edges = EdgeSelector.select_edges(shell)
    if not edges:
        break
    if EdgeModifier.update_edge_attributes(shell, edges):
        shell.fofin()
        redraw()


# ==============================================================================
# Visualise the result
# ==============================================================================

artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.draw_faces()
artist.draw_loads()
artist.draw_residuals()
