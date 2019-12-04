# Assignment-RA2

Assignment for the second lesson on Robotic Assembly

## Task 1: Assembly

Create a brick assembly with a single flemish bond. Use the file `01_flemish_bond.py` as a starting point. At the end, this script serialises your assembly into `flemish_bond.json` in the `data` folder.

It's probably best to develop the code in RhinoPythonEditor to immediately see the result. Alternatively, you can also load the assembly in Grasshopper using `02_visualise_flemish_bond_ghpython.ghx`.

Have a look into example nr. 27 in the examples folder of module 2 of the `ita19` repository.

## Task 2: Planning

Now plan paths by filling in the missing code lines of `03_plan_paths_for_assembly.py`. The point here is to add collision objects to the planning scene, define picking and target frames, etc.

You will load the assembly from the saved json file and start iterating over all bricks in the assembly. For each brick calculate picking, moving and placing trajectories and add the placed brick to the planning scene.

You might sometimes get an error (`compas_fab.backends.ros.exceptions.RosValidationError: Error code: -1; PLANNING_FAILED`) which happens from time to time. Don't worry, just rerun the file, it would load the assembly from `flemish_bond_planned.json` and would skip the bricks that are already planned. However, if the error appears every time at the same brick, you might check the brick walls' location or height.

Have a look into example nr. 26 in the examples folder of module 2 of the `ita19` repository.

<div align="center"><br><img src="https://raw.githubusercontent.com/compas-ITA19/ITA19/master/modules/module2/images/assignment2_1.jpg" width="600" /></div>
