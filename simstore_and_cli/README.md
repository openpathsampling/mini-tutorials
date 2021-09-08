# Using SimStore and the OpenPathSampling CLI

This tutorial covers two recent (added in 2020) developments for
OpenPathSampling. These are the new (experimental) storage subsystem, called
SimStore, and the command line interface to OPS.

Note that these topics are independent -- the CLI can also be used with the old
storage subsystem (NetCDFPlus) and SimStore can be used without the CLI.
However, performance improvements in SimStore make it much more convenient for
the kind of interactivity enabled by the CLI.

In OPS 2.0, NetCDFPlus will be removed and SimStore will be used for all storage.

## Videos

This tutorial was presented as a series of three YouTube videos. You can watch
them in the playlist for this tutorial [COMING SOON], or you can watch each part:

* [Part 1: Setting up with SimStore](https://www.youtube.com/watch?v=IAipZfZpwZ4)
* [Running simulations with the CLI](https://www.youtube.com/watch?v=VGN-NfuZGqY)
* COMING SOON: Part 3: Analyzing the results

## Requirements

This tutorial requires OpenPathSampling 1.5 or later and the OpenPathSampling
CLI 0.2 or later. In addition, it requires OpenMM and OpenMMTools. Finally,
SQLAlchemy and dill must be installed for SimStore to work.

Install the requirements with:

```bash
conda install -c conda-forge openpathsampling openpathsampling-cli
conda install -c conda-forge openmm openmmtools
conda install -c conda-forge sqlalchemy dill
```

In addition, you will need about 500 MB of disk space available.

## Running the tutorial

The tutorial consists of Jupyter notebooks (for setup and analysis) as well as
a Markdown file describing what needs to be done to run with the CLI. We
recommend either using a terminal within JupyterLab to run the CLI commands, or
keeping a separate terminal open on your system.

The tutorial can also be run on Binder, via its JupyterLab interface. 

The setup process is described in the notebook `1_simstore_setup.ipynb`. The
process of using the CLI is described in `2_running_cli.md`. The analysis is performed
in `3_analysis.ipynb`.
