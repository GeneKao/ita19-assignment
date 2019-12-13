from math import pi

from compas_fab.rhino import RobotArtist
from compas_fab.robots import Configuration

from compas.datastructures import Mesh
from compas.geometry import Circle, Cylinder, Frame, Plane, Translation
from compas.robots import Joint, RobotModel
from random import random

# Create cylinder in yz plane for all robot link's visual_mesh
radius, length = 1, 10
cylinder = Cylinder(Circle(Plane([0, 0, 0], [1, 0, 0]), radius), length)
cylinder.transform(Translation([length / 2., 0, 0]))
mesh = Mesh.from_shape(cylinder)

# Add all other links to robot
names = []
link_count = 10

for count in range(1, link_count):
    if count == 1:
        robot = RobotModel("robot", links=[], joints=[])
        robot.add_link("world", visual_mesh=mesh.copy(),
                       visual_color=(0, 0, 0))
    else:
        # add new link to robot
        robot.add_link("link" + str(count), visual_mesh=mesh.copy(),
                       visual_color=(random(), random(), random()))
        # add the joint between the last two link
        origin = Frame((length, 0, 0), (1, 0, 0), (0, 1, 0))
        robot.add_joint("joint" + str(count), Joint.CONTINUOUS, robot.links[-2],
                        robot.links[-1], origin, (0, 0, 1))
        names.append("joint" + str(count))

# visualize the robot to move z zag shape
artist = RobotArtist(robot)
angles = [0.1 if i % 2 == 0 else -0.1 for i in range(len(names))]

for step in range(25):
    angles = [a + 0.1 if i % 2 == 0 else a - 0.1 for i, a in enumerate(angles)]
    config = Configuration.from_revolute_values(angles)
    artist.update(config, names)
    artist.draw_visual()
    artist.redraw(0.1)
