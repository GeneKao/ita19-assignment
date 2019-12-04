import os
from assembly import Assembly
from assembly.rhino import AssemblyArtist

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "data"))

filepath = os.path.join(DATA, 'flemish_bond.json')
assembly = Assembly.from_json(filepath)

artist = AssemblyArtist(assembly, layer='COMPAS::Assembly')
artist.clear_layer()
artist.draw()
