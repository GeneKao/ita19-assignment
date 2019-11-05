from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import add_vectors
from compas.geometry import scale_vector

import compas_rhino
from compas_rhino.artists import MeshArtist

__all__ = ["ShellArtist"]

class ShellArtist(MeshArtist):
    
    def draw_loads(self, scale=1.0, layer="Selfweight::Loads"):
        loads = []
        for key in self.datastructure.vertices():
            if self.datastructure.get_vertex_attribute(key, 'is_fixed'):
                continue
            load = self.datastructure.get_vertex_attributes(key, ('px', 'py', 'pz'))
            vector = scale_vector(load, scale)
            start = self.datastructure.vertex_coordinates(key)
            end = add_vectors(start, vector)
            loads.append({
                'start': start,
                'end': end,
                'arrow': 'end',
                'color': (0, 0, 255)})
        compas_rhino.draw_lines(loads, layer=layer, clear=False)

    def draw_residuals(self, scale=1.0, layer="Selfweight::Residuals"):
        residuals = []
        for key in self.datastructure.vertices():
            if self.datastructure.get_vertex_attribute(key, 'is_fixed'):
                continue
            residual = self.datastructure.get_vertex_attributes(key, ('rx', 'ry', 'rz'))
            vector = scale_vector(residual, scale)
            start = self.datastructure.vertex_coordinates(key)
            end = add_vectors(start, vector)
            residuals.append({
                'start': start,
                'end': end,
                'arrow': 'end',
                'color': (0, 255, 255)})
        compas_rhino.draw_lines(residuals, layer=layer, clear=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
