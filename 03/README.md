# Structural Design: Assignment 1

## Part 1: Update selfweight

*Use selfweight.py as a starting point for this part of the assignment.*

Until now, we have only included prestress during the form finding of the equilibrium geometry of form-active strctures like cable nets.

The objective of this part of the assignment is to include selfweight in the form finding process.

**Apply selfweight as load**

Loads are applied on the vertices of the mesh.
To apply the selfweight as load, you have to calculate how much of it has to be asigned to each vertex.
The part of the mesh surface that corresponds to a particular vertex is called the tributary area of that vertex.

The `Mesh` data structure has a method to compute the area per vertex: `Mesh.vertex_area`.
The selfweight of the structure at that vertex can be computed by multiplying the area by a thickness value.
You can use a constant thickness value or update the default vertex attributes with a thickness parameter and assign a thickness per vertex.

*Steps:*

1. Compute the weight on every vertex.
2. Assign the weight to the list of loads.
3. Compute equilibrium.
4. Update the data structure.
5. Visualise the new geometry and the loads.

```python
area = mesh.vertex_area(key)
weight = area * thickness
loads[key][2] = -weight
```

**Compute residual forces**

Note that the updated geometry is in equilibrium with the selfweight of the previous geometry.

Write a function to compute the unbalanced forces after the selfweight is updated using the updated geometry.

*Steps:*

1. Compute the weight of every vertex.
2. Compute the resultant of the forces in the edges connected to every vertex and the updated load.

```python
load = [0.0, 0.0, -weight]
forces = [load]
for nbr in mesh.vertex_neighbors(key):
    # compute the force vector of the connected edge
    forces.append(force)
resultant = sum_vectors(forces)
```

## Part 2: Update cables

The objective of this part of the assignment is to update the force densities of all edges belonging to a cable at once, rather than updating them one by one.

To select an edge of the mesh in Rhino:

```python
from compas_rhino.selectors import EdgeSelector
edge = EdgeSelector.select_edge(mesh)
```

To update the attributes of selected edges in Rhino:

```python
from compas_rhino.modifiers import EdgeModifier
if EdgeModifier.update_edge_attributes(mesh, edges):
    # success => do something
```

*Steps:*

First write a function to find all edges of the cable corresponding to a selected edge.

1. Select edge.
2. Find cable edges.
3. Update edge attributes.
4. Compute a new equilibrium geometry.
5. Visualise the result.
