from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import scale_vector
from compas.geometry import normalize_vector
from compas.geometry import sum_vectors

from compas.datastructures import Mesh
from compas.rpc import Proxy

numerical = Proxy('compas.numerical')
fd_numpy = numerical.fd_numpy

__all__ = ["Shell"]

class Shell(Mesh):

    def __init__(self):
        super(Shell, self).__init__()
        self.update_default_vertex_attributes({
            'px': 0.0,
            'py': 0.0,
            'pz': 0.0,
            'rx': 0.0,
            'ry': 0.0,
            'rz': 0.0,
            't': 0.1,
            'is_fixed': False})

        self.update_default_edge_attributes({
            'q': 1.0,
            'f': 0.0,
            'l': 0.0})

    def fofin(self):

        corners = list(self.vertices_where({'vertex_degree': 2}))
        self.set_vertices_attribute('is_fixed', True, keys=corners)
        fixed = list(self.vertices_where({'is_fixed': True}))
        high = [0, 35]
        self.set_vertices_attribute('z', 7.0, keys=high)
        boundary = list(self.edges_on_boundary())
        self.set_edges_attribute('q', 5.0, keys=boundary)

        count = 0
        threshold = 0.001
        while True:
            print('iteration: ', count)
            # compile the input for fd_numpy
            xyz = self.get_vertices_attributes('xyz')
            edges = list(self.edges())
            q = self.get_edges_attribute('q')
            loads = self.get_vertices_attributes(('px', 'py', 'pz'))

            for key in self.vertices():
                if self.get_vertex_attribute(key, 'is_fixed'):
                    continue

                thickness = self.get_vertex_attribute(key, 't')
                # compute the vertex area
                area = self.vertex_area(key)
                # multiply by the local thickness
                weight = area * thickness
                # assign to the correct item in the list of loads
                loads[key][2] = -weight
                self.set_vertex_attributes(key, ('px', 'py', 'pz'), [0, 0, -weight])

            xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

            terminate = True
            # update the data structure
            for key, attr in self.vertices(True):

                if abs(attr['x'] - xyz[key][0]) > threshold or \
                        abs(attr['y'] - xyz[key][1]) > threshold or \
                        abs(attr['z'] - xyz[key][2]) > threshold:
                    terminate = terminate and False
                else:
                    terminate = terminate and True

                attr['x'] = xyz[key][0]
                attr['y'] = xyz[key][1]
                attr['z'] = xyz[key][2]
                attr['rx'] = r[key][0]
                attr['ry'] = r[key][1]
                attr['rz'] = r[key][2]

            if terminate and count >= 2:
                print('solution found')
                break

            for index, (u, v, attr) in enumerate(self.edges(True)):
                attr['f'] = f[index][0]

            for key in self.vertices():
                if self.get_vertex_attribute(key, 'is_fixed'):
                    continue

                # compute the load on the vertex
                load = loads[key]
                # compute the forces in the edges connected to the vertex
                forces = [load]
                for nbr in self.vertex_neighbors(key):
                    # compute the force vector of the connected edge
                    force = [a - b for a, b in zip(self.get_vertex_attributes(nbr, 'xyz'),
                                                   self.get_vertex_attributes(key, "xyz"))]
                    length = self.get_edge_attribute((key, nbr), 'f')
                    force = scale_vector(normalize_vector(force), length * 2)
                    forces.append(force)

                # sum up the vectors to compute the residual force
                resultant = sum_vectors(forces)
                self.set_vertex_attributes(key, ('rx', 'ry', 'rz'), resultant)

            count += 1
            # put a safety break here
            if count > 30:
                print("too many iterations")
                break


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
