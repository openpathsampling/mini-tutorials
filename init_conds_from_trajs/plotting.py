"""
Custom plotting methods for this tutorial.
"""

from matplotlib import pyplot as plt
import openpathsampling as paths

cv = paths.CoordinateFunctionCV('CV', lambda s: s.xyz[0][0])

def _plot_background(ax):
    ax.axhline(1.0, color='r', zorder=-10)
    ax.axhline(0.0, color='r', zorder=-10)
    ax.set_ylabel(cv.name)
    ax.set_xlabel('time (frame number)')
    ax.set_ylim(-0.1, 1.1)

def _plot_traj(ax, traj):
    if isinstance(traj, paths.Sample):
        traj, label = traj.trajectory, traj.ensemble.name
    elif isinstance(traj, paths.Trajectory):
        traj, label = traj, 'Input trajectory'
    else:
        raise RuntimeError("Something went wrong")

    ax.plot(cv(traj), 'o-', label=label)

def add_interfaces(ax, interfaces):
    for iface in interfaces:
        ax.axhline(iface, ls=':', color='r', lw=0.5)

def plot(inputs, outputs=None, interfaces=None):
    if outputs is None:
        fig, ax = plt.subplots(1, 1, figsize=(5, 4))
        axs = [ax]
    else:
        fig, axs = plt.subplots(1, 2, figsize=(11, 4))

    if isinstance(inputs, paths.Trajectory):
        inputs = [inputs]

    for ax, inp in zip(axs, [inputs, outputs]):
        _plot_background(ax)
        for traj in inp:
            _plot_traj(ax, traj)
        if interfaces is not None:
            add_interfaces(ax, interfaces)
        if inputs:
            ax.legend()
        else:
            ax.set_xlim(0, 10)
