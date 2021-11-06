This mini-tutorial deals with two tools for setting up simulations using the
OpenPathSampling CLI: the Wizard and the `compile` command.


## Requirements

This tutorial requires OpenPathSampling, the OpenPathSampling CLI, OpenMM, and
OpenMMTools.

## Alanine dipeptide

The system we will study is alanine dipeptide. It's a boring, simple system,
but one that you can easily run on a laptop, and one that illustrates the
basics of path sampling very well.

In this mini-tutorial, we provide the necessary (solvated and equilibrated)
inputs to run TPS. To learn how to set up an OpenMM simulation, we recommend
the [OpenMM documentation](http://docs.openmm.org). To learn how to get an
initial trajectory for path sampling simulations, we have several other
tutorials, such as the `simstore_and_cli` tutorial in this repository. Simple
scripts to generate the necessary files (requiring OpenMMTools) are provided in
the `prereqs` directory.


## Target TPS setup

* **Engine**: The engine should use the provided PDB for topology, and the
  provided integrator and system XML files. That integrator uses a 2 fs
  timestep; you should save frames every 20 fs, and abort any trajectory that
  runs for 20 ps. (Note: timescales for practical biomolecular systems are
  usually much longer, saving frames on the order of every picosecond and
  allowing trajectories of 10s or even 100s of nanoseconds.)
* **CVs**: The CVs we use here are the phi and psi dihedral angles. The atoms
  that define them (counting from 0) are:

  * *phi*: 4, 6, 8, 14
  * *phi*: 6, 8, 14, 16

  To learn how to identify those atom numbers in practice, we recommend the
  [Python-based tutorial](http://github.com/openpathsampling/ops_tutorial),
  which shows how to use MDTraj to identify them.

* **States**: We'll look at the transition from the `C_7eq` state to the
  `alpha_R` state. These states are defined by the following (in degrees):

  * `C_7eq`: -180 <= phi < 0  and 100 <= psi < 200
  * `alpha_R`: -180 <= phi < 0 and -100 <= psi < 0

  Note that these are in degrees; since MDTraj reports dihedrals in radians,
  you'll need to scale these numbers by pi/180 to get radians.

* **TPS Details**: When setting up with the Wizard, use uniform shooting point
  selection. When setting up with the ``compile`` command, an example with
  uniform shooting point selection is already provided, and you should create a
  second option with a Gaussian biased shooting point selection based on the
  `psi` variable, with mean at 50 degrees and standard deviation 10 degrees.

## Using the Wizard

First, we recommend using the OPS Wizard to set up this simulation. The Wizard
will guide you through every step necessary to set up the simulation. Start the
Wizard with the command `openpathsampling wizard`.

## Using the `compile` command

For the part of this tutorial with the compile command, 
