# Running with the CLI

## Finding your way around the CLI

Once you've installed the OpenPathSampling CLI (via pip or conda-forge, package
name `openpathsampling-cli`), the command `openpathsampling` is available at
your regular shell prompt. The OPS CLI consists of multiple subcommands, and
we'll use several of them in this tutorial. To get more information, use the
`-h` or `--help` flag. For example, to get a listing of subcommands, use the
command:

```bash
openpathsampling --help
```

which will give output something like:

```text
Usage: openpathsampling [OPTIONS] COMMAND [ARGS]...

  OpenPathSampling is a Python library for path sampling simulations. This
  command line tool facilitates common tasks when working with
  OpenPathSampling. To use it, use one of the subcommands below. For example,
  you can get more information about the pathsampling tool with:

      openpathsampling pathsampling --help

Options:
  --log PATH  logging configuration file
  -h, --help  Show this message and exit.

Simulation Commands:
  visit-all     Run MD to generate initial trajectories
  md            Run MD for fixed time or until a given ensemble is satisfied
  equilibrate   Run equilibration for path sampling
  pathsampling  Run any path sampling simulation, including TIS variants

Miscellaneous Commands:
  contents     list named objects from an OPS .nc file
  append       add objects from INPUT_FILE  to another file
```

Most subcommands have arguments that can take the name of named OPS objects (such
as engines, state volumes, etc.), and therefore require the name of an input
file where those objects can be found. The `contents` subcommand is very useful
for seeing the list of named objects in a file. For example, after creating
`setup.db` as described in the first notebook in this tutorial, try the
command:

```bash
openpathsampling contents setup.db
```

This will provide information about the objects stored in that file.

## Overview

In the first notebook in this tutorial, we set up everything to describe our
path sampling simulation, but we only have a single snapshot of our system. The
initial conditions for path sampling simulations are a set of trajectories. In
order to obtain the necessary trajectories, we will use several tools in the
OPS CLI to help generate valid initial conditions.

Overall, we'll go through the following process:

1. Use a high temperature engine to generate a trajectory that connects our
   stable states. If it connects the stable states, it is guaranteed to cross
   all TIS interfaces.
2. Extend that trajectory to also satisfy any missing minus interfaces.
3. Equilibrate those unphysical trajectories to a reasonable physical
   trajectory.
4. Perform our production run.

## Initial trajectories for TIS (or TPS)

Obtaining initial trajectories is one of the tricky aspects of path sampling,
and how you do it will depend on your system.  Here, we will use
high-temperature molecular dynamics to do that, although other approaches (such
as using a first crossing from metadynamics) are also quite practical.

OpenPathSampling has a convenient tool called the `VisitAllStatesEnsemble`,
which runs dynamics until all given states have been visited. This ensemble
also provides feedback on progress. This is particularly useful for multiple
state transition interface sampling, because a trajectory that has visited all
states is guaranteed to have subtrajectories that meet the requirements of
every TIS ensemble in MSTIS. This is also true for any two-state system, such
as the one we are studying here.

To generate a trajectory with the `VisitAllStatesEnsemble`, use the `visit-all`
subcommand. You can investigate it's options with `openpathsampling visit-all
--help`: we will need to provide the name of an engine, the names of the
states, and an output file. In principle, we would need to provide an initial
frame as well, but OPS can infer the initial conditions since there is only one
snapshot saved to storage.

```bash
openpathsampling visit-all setup.db -s condensed -s extended -e hi_temp -o visit-all.db
```

The resulting trajectory is saved in the file `visit-all.db` with the tag
`final_conditions`. If we want to copy that trajectory to `setup.db`, we can
use the `append` subcommand. We will change the tag name it is saved under to
`long_traj`:

```bash
openpathsampling append visit-all.db -a setup.db --tag final_conditions --save-tag long_traj
```

## Filling in the minus interface ensemble

At this point, if we tried to run the final `pathsampling` command (or even the
`equilibrate` command) we would get an error:

```pytb
AssertionError: Bad initial conditions.
Missing ensembles:
*  [condensed MIS minus]
```

This is because our TIS network includes a minus ensemble associated with the
condensed state. Since our `visit-all` simulation started in the extended
state, it stopped as soon as it found its first frame in the condensed state.
No subtrajectory of that trajectory will meet the requirements of the minus ensemble.

However, by running dynamics starting in that last frame, we will (very likely)
obtain a trajectory that satisfies minus ensemble. (Note that there is a small
chance that the trajectory will spontaneously cross to the other state, which
would not satisfy the minus ensemble.)

While this could be done by running standard MD for a fixed period of time, and
checking if the resulting trajectory met the minus ensemble requirements, the
OPS CLI provides an easier approach: the `md` subcommand, which can run MD for
either a fixed time or until a given ensemble's criteria are met.

The `md` subcommand will require that we provide the ensemble name, the engine,
and the initial frame. Since we happen to know that the frame we want is the
last one that was saved, we can select it with `-1`. For the ensemble, we can
see the name that was listed as missing in the error, or we can use the command
`openpathsampling contents setup.db --table ensembles` to see all the named
ensembles in our setup file. Noting that the ensemble name should be in quotes
(to preserve the spaces), the command to run the MD is:

```bash
openpathsampling md setup.db -o minus-traj.db -e engine -f -1 --ensemble "condensed MIS minus"
```

We can then copy the resulting trajectory to `setup.db` with

```bash
openpathsampling append minus-traj.db -a setup.db --tag final_conditions --save-tag minus_traj
```

## Equilibrating

Now we're ready to equilibrate our initial conditions before performing path
sampling. By running `openpathsampling equlibrate --help`, we see that, in
addition to input and output files, we need a move scheme and initial
conditions, and we can optionally provide a "multiplier" and a number of "extra
steps."

The `equilibrate` subcommand runs until all frames from the initial conditions
have been replaced by new, dynamically generated frames. This means that the
unphysical high-temperature frames will be removed and replaced by frames
generated at the correct temperature. Note that this is a bare minimum for
reasonable initial conditions -- this does necessarily mean that the
trajectories have sufficiently decorrelated.

Additional decorrelation can be provided by the `--multiplier` and
`--extra-steps` arguments. If that bare minimum decorrelation takes N steps,
and the options `--multiplier 2` and `--extra-steps 10` are given, then the
total number of path sampling steps run during equilibration will be 2*N + 10.

We can select the conditions saved in tags as initial conditions to
decorrelate. We can provide the `-t`/`--init-conds` flag more than once, and we
will do so for the saved tags `long_traj` and `minus_traj`.

Because only one move scheme is saved in `setup.db`, the `equilibrate`
subcommand implicitly knows to use that scheme, and we don't have to specify it
on the command line. The command to equilibrate for the minimum number of steps
is then:

```bash
openpathsampling equilibrate setup.db -t long_traj -t minus_traj -o equil.db
```

The results of this are the initial conditions for our production run, and
we'll copy them over to `setup.db` with the tag name `'initial_conditions'`:

```bash
openpathsampling append equil.db -a setup.db --tag final_conditions --save-tag initial_conditions
```


## Production run

Finally, we do the production run. Like `equilibrate`, the production
`pathsampling` command can implicitly figure out the move scheme to use.
Additionally, since we gave our initial conditions the special tag name
`'initial_conditions'`, the CLI will use that as the initial conditions. Therefore, we only need to specify the input file, the output file, and the number of Monte Carlo steps to run:

```bash
openpathsampling pathsampling setup.db -o tis.db --nsteps 5000
```
