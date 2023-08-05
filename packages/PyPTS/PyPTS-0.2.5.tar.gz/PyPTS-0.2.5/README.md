# PyPTS: A Python Plant Tissue Simulation tools

PyPTS is a Python package for creating cell-based simulations of plant tissue.
It provides the basic building blocks for prototyping and running small to
medium scale simulations of two dimensional plant tissues. 

- Author: Przemyslaw Klosiewicz (przemek.klosiewicz@gmail.com)
- License: BSD 3-Clause, cfr. `LICENSE.txt`

## Installation

The standard way of installing PyPTS is either through `pip`:

    pip install PyPTS

or downloading the sources / cloning the repository and running:

    python ./setup.py install [--user]

inside the PyPTS source tree.

### Requirements

Currently used versions are indicated. Code possibly works with slightly older
versions as well.

- Python 2.7
- NumPy (Used all throughout the code)
- SciPy (Maily for the solvers)
- h5py (I/O for tissue files)
- Matplotlib (Plotting tissue structures)
- PySide (optional; for `tissue_plot.py` visualization)
- MPI4Py (optional; for running bulk sweep jobs, cfr: `mpi_*.py`)

## Usage

See `pypts/examples` for some example scripts

